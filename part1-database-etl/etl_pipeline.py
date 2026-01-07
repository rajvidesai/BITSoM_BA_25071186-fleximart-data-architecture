# etl_pipeline.py
"""
FlexiMart ETL Pipeline
Extracts raw CSV data, cleans it, and loads into MySQL database.
Generates a data quality report.
"""

import pandas as pd
import mysql.connector
from datetime import datetime

# -----------------------------
# DATABASE CONFIGURATION
# -----------------------------

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root123",
    "database": "fleximart"
}


# -----------------------------
# DATA QUALITY METRICS
# -----------------------------
report = {
    "customers": {"processed": 0, "duplicates": 0, "missing": 0, "loaded": 0},
    "products": {"processed": 0, "duplicates": 0, "missing": 0, "loaded": 0},
    "sales": {"processed": 0, "duplicates": 0, "missing": 0, "loaded": 0},
}

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def standardize_phone(phone):
    if pd.isna(phone):
        return None
    digits = ''.join(filter(str.isdigit, str(phone)))
    return f"+91-{digits[-10:]}" if len(digits) >= 10 else None


def standardize_category(cat):
    return str(cat).strip().capitalize()


def parse_date(date_val):
    try:
        return pd.to_datetime(date_val).date()
    except Exception:
        return None


# -----------------------------
# DATABASE CONNECTION
# -----------------------------
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# -----------------------------
# EXTRACT & TRANSFORM: CUSTOMERS
# -----------------------------
# 
customers = pd.read_csv("customers_raw.csv")

# Remove completely empty rows (fixes extra count issue)
customers.dropna(how="all", inplace=True)

# Count raw records correctly
report["customers"]["processed"] = len(customers)

# Remove duplicates
before_dedup = len(customers)
customers.drop_duplicates(inplace=True)
report["customers"]["duplicates"] = before_dedup - len(customers)

# Standardize phone and date
customers["phone"] = customers["phone"].apply(standardize_phone)
customers["registration_date"] = customers["registration_date"].apply(parse_date)

# Handle missing email
missing_before = customers.isnull().sum().sum()
customers.dropna(subset=["email"], inplace=True)
missing_after = customers.isnull().sum().sum()
report["customers"]["missing"] = missing_before - missing_after


# -----------------------------
# LOAD: CUSTOMERS
# -----------------------------
for _, row in customers.iterrows():
    try:
        # cursor.execute("""
        #     INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
        #     VALUES (%s, %s, %s, %s, %s, %s)
        # """, tuple(row))
        cursor.execute("""
    INSERT INTO customers
    (first_name, last_name, email, phone, city, registration_date)
    VALUES (%s, %s, %s, %s, %s, %s)
""", (
    row["first_name"],
    row["last_name"],
    row["email"],
    row["phone"],
    row["city"],
    row["registration_date"]
))

        report["customers"]["loaded"] += 1
    except Exception:
        conn.rollback()

conn.commit()

# -----------------------------
# EXTRACT & TRANSFORM: PRODUCTS
# -----------------------------
products = pd.read_csv("products_raw.csv")
report["products"]["processed"] = len(products)

products.drop_duplicates(inplace=True)
report["products"]["duplicates"] = report["products"]["processed"] - len(products)

products["price"].fillna(0.0, inplace=True)
products["stock_quantity"].fillna(0, inplace=True)
products["category"] = products["category"].apply(standardize_category)

report["products"]["missing"] = products.isnull().sum().sum()

# -----------------------------
# LOAD: PRODUCTS
# -----------------------------
for _, row in products.iterrows():
    # cursor.execute("""
    #     INSERT INTO products (product_name, category, price, stock_quantity)
    #     VALUES (%s, %s, %s, %s)
    # """, tuple(row))
    cursor.execute("""
    INSERT INTO products
    (product_name, category, price, stock_quantity)
    VALUES (%s, %s, %s, %s)
""", (
    row["product_name"],
    row["category"],
    row["price"],
    row["stock_quantity"]
))

    report["products"]["loaded"] += 1

conn.commit()

# -----------------------------
# EXTRACT & TRANSFORM: SALES
# -----------------------------
sales = pd.read_csv("sales_raw.csv")
report["sales"]["processed"] = len(sales)

sales.drop_duplicates(inplace=True)
report["sales"]["duplicates"] = report["sales"]["processed"] - len(sales)

#sales["order_date"] = sales["order_date"].apply(parse_date)
sales["transaction_date"] = sales["transaction_date"].apply(parse_date)

sales.dropna(subset=["customer_id", "product_id"], inplace=True)

report["sales"]["missing"] = sales.isnull().sum().sum()

# -----------------------------
# LOAD: SALES → ORDERS & ORDER_ITEMS
# -----------------------------
# for _, row in sales.iterrows():
#     cursor.execute("""
#         INSERT INTO orders (customer_id, order_date, total_amount)
#         VALUES (%s, %s, %s)
#     """, (row["customer_id"], row["transaction_date"], row["total_amount"]))
#     order_id = cursor.lastrowid

#     cursor.execute("""
#         INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
#         VALUES (%s, %s, %s, %s, %s)
#     """, (
#         order_id,
#         row["product_id"],
#         row["quantity"],
#         row["unit_price"],
#         row["quantity"] * row["unit_price"]
#     ))

#     report["sales"]["loaded"] += 1

# conn.commit()

# -----------------------------
# SALES → ORDERS + ORDER_ITEMS
# -----------------------------
sales = pd.read_csv("sales_raw.csv")

sales.drop_duplicates(inplace=True)

# Convert CSV date column
sales["transaction_date"] = sales["transaction_date"].apply(parse_date)

# Drop rows with missing IDs
sales.dropna(subset=["customer_id", "product_id"], inplace=True)

for _, row in sales.iterrows():
    try:
        total_amount = row["quantity"] * row["unit_price"]

        # Insert into orders table
        cursor.execute("""
            INSERT INTO orders (customer_id, order_date, total_amount)
            VALUES (%s, %s, %s)
        """, (
            row["customer_id"],
            row["transaction_date"],
            total_amount
        ))

        order_id = cursor.lastrowid

        # Insert into order_items table
        cursor.execute("""
            INSERT INTO order_items
            (order_id, product_id, quantity, unit_price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            order_id,
            row["product_id"],
            row["quantity"],
            row["unit_price"],
            total_amount
        ))

    except Exception as e:
        print("Sales insert failed:", e)
        conn.rollback()

conn.commit()


# -----------------------------
# DATA QUALITY REPORT
# -----------------------------
with open("data_quality_report.txt", "w") as f:
    for table, stats in report.items():
        f.write(f"{table.upper()} DATA\n")
        for k, v in stats.items():
            f.write(f"{k}: {v}\n")
        f.write("\n")

cursor.close()
conn.close()

print("ETL Pipeline Completed Successfully")
