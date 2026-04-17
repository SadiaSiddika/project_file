import os
import sqlite3
import pandas as pd

# ---------------- Set file paths ----------------
# Folder where you want to save the CSV
save_folder = r"E:\finalproject_web309_2026"

# Make sure the folder exists
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# CSV file path
csv_file_path = os.path.join(save_folder, "diagnosis_history.csv")

# SQLite database file path (replace with your actual db location if needed)
db_file_path = r"E:\finalproject_web309_2026\thyroscan.db"

# ---------------- Connect to database ----------------
try:
    conn = sqlite3.connect(db_file_path)
    print("Connected to database:", db_file_path)
except Exception as e:
    print("Error connecting to database:", e)
    exit()

# ---------------- Read table ----------------
try:
    df = pd.read_sql_query("SELECT * FROM diagnosis_history", conn)
    print("Data read successfully. Number of rows:", len(df))
except Exception as e:
    print("Error reading table:", e)
    exit()
finally:
    conn.close()

# ---------------- Export to CSV ----------------
try:
    df.to_csv(csv_file_path, index=False)
    print("CSV file saved successfully at:", csv_file_path)
except Exception as e:
    print("Error saving CSV file:", e)