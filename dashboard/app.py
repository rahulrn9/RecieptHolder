
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.storage.db import init_db, insert_receipt, fetch_all_receipts
from backend.ingestion.validate import ReceiptFile
from backend.parsing.parser import parse_image, parse_pdf, parse_text_file, extract_fields
from backend.sync.google_sync import sync_receipt_to_sheet  # ✅ Google Sheets Sync

import streamlit as st
import pandas as pd
from datetime import datetime

# Init DB
init_db()

# Load data
df = fetch_all_receipts()

# Sidebar Navigation
with st.sidebar:
    st.title("📊 Receipt Analyzer")
    page = st.radio("Navigate", ["📤 Upload", "📋 Records", "📈 Analytics", "📁 Export"])

st.set_page_config(page_title="Receipt Analyzer", layout="wide")

# -------------------------------
# 📤 Upload Page
# -------------------------------
if page == "📤 Upload":
    st.title("📤 Upload Receipt")
    uploaded_file = st.file_uploader("Upload (.pdf, .jpg, .png, .txt)", type=["pdf", "jpg", "jpeg", "png", "txt"])

    if uploaded_file:
        path = f"data/{uploaded_file.name}"
        with open(path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        file_ext = uploaded_file.name.split(".")[-1].lower()
        validator = ReceiptFile(file_path=path, file_type=file_ext)

        if file_ext in ["jpg", "jpeg", "png"]:
            text = parse_image(path)
        elif file_ext == "pdf":
            text = parse_pdf(path)
        else:
            text = parse_text_file(path)

        with st.expander("📝 Parsed Text Preview"):
            st.text_area("Extracted Text", text, height=200)

        # 🧠 ML field extraction + category prediction
        vendor, date, amount, category, confidence = extract_fields(text)

        st.markdown(f"**Vendor**: `{vendor}`")
        st.markdown(f"**Date**: `{date}`")
        st.markdown(f"**Amount**: `₹{amount}`")
        st.markdown(f"**Predicted Category (ML)**: 🧠 `{category}` with `{confidence*100:.2f}%` confidence")

        # 🔧 Manual override
        override = st.selectbox("🔧 Override Category (optional)",
                                options=["", "Grocery", "Electricity", "Internet", "Health", "Other"],
                                index=0)
        final_category = override if override else category

        sync_toggle = st.checkbox("🔄 Also sync to Google Sheet")

        if st.button("✅ Save to Database"):
            insert_receipt(vendor, date, amount, final_category)
            st.success("💾 Saved to local database!")

            if sync_toggle:
                try:
                    sync_receipt_to_sheet(vendor, date, amount, final_category)
                    st.success("🔄 Synced to Google Sheet!")
                except Exception as e:
                    st.error(f"❌ Google Sheet sync failed: {e}")

# -------------------------------
# 📋 Records Page
# -------------------------------
elif page == "📋 Records":
    st.title("📋 All Receipts")
    st.dataframe(df, use_container_width=True)

    if not df.empty:
        with st.expander("🔢 Summary Metrics"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Spend", f"₹{df['amount'].sum():,.2f}")
            col2.metric("Top Vendor", df["vendor"].value_counts().idxmax())
            col3.metric("Total Entries", len(df))

# -------------------------------
# 📈 Analytics Page
# -------------------------------
elif page == "📈 Analytics":
    st.title("📈 Spend Analytics")

    if df.empty:
        st.warning("No data available. Upload receipts first.")
    else:
        tab1, tab2 = st.tabs(["📊 Top Vendors", "📅 Spend Over Time"])

        with tab1:
            st.subheader("📊 Vendor Frequency")
            st.bar_chart(df["vendor"].value_counts())

        with tab2:
            df["parsed_date"] = pd.to_datetime(df["date"], errors='coerce')
            monthly = df.dropna(subset=["parsed_date"]).groupby(df["parsed_date"].dt.to_period("M"))["amount"].sum()
            monthly.index = monthly.index.to_timestamp()
            st.line_chart(monthly)

# -------------------------------
# 📁 Export Page
# -------------------------------
elif page == "📁 Export":
    st.title("📁 Export Data")

    if df.empty:
        st.warning("Nothing to export.")
    else:
        st.download_button("📥 Download CSV", df.to_csv(index=False), "receipts.csv", "text/csv")
        st.download_button("📥 Download JSON", df.to_json(orient="records"), "receipts.json", "application/json")
