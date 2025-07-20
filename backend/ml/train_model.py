import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import os

# Ensure directory exists
os.makedirs("backend/ml", exist_ok=True)

# Sample training data
data = [
    ("FreshMart", "Milk Bread Grocery Store Purchase", "Grocery"),
    ("PowerGrid", "Electricity Bill Units Charges", "Electricity"),
    ("JioFiber", "Broadband Internet Recharge Plan", "Internet"),
    ("Apollo Pharmacy", "Prescription Medical Pharmacy Health", "Health"),
    ("Spencer's", "Rice Dal Vegetables Grocery Items", "Grocery"),
    ("Bescom", "Power Charges Bill Electricity Usage", "Electricity"),
    ("Airtel", "Internet Fiber Plan Recharge Monthly", "Internet"),
    ("Max Hospital", "Medical Hospital Bill Health Checkup", "Health"),
]

# Convert to DataFrame
df = pd.DataFrame(data, columns=["vendor", "text", "category"])
df["combined"] = df["vendor"] + " " + df["text"]

# Build pipeline
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("nb", MultinomialNB())
])

# Train and save model
pipeline.fit(df["combined"], df["category"])
joblib.dump(pipeline, "backend/ml/category_model.pkl")

print("✅ Model retrained and saved.")
