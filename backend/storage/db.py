import sqlite3
import pandas as pd
import os

# 🔧 Ensure the data/ folder exists before connecting to DB
os.makedirs('data', exist_ok=True)

DB_PATH = 'data/receipts.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor TEXT,
            date TEXT,
            amount REAL,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_receipt(vendor, date, amount, category=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO receipts (vendor, date, amount, category)
        VALUES (?, ?, ?, ?)
    ''', (vendor, date, amount, category))
    conn.commit()
    conn.close()

def fetch_all_receipts():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM receipts", conn)
    conn.close()
    return df
