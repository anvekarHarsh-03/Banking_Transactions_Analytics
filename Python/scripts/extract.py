import pandas as pd
import mysql.connector
from config import DB_CONFIG

def extract():
    print("  [EXTRACT] Reading raw CSV...")
    df = pd.read_csv("dataset/raw_transactions.csv", dtype=str)
    print(f"  -> {len(df)} records read from CSV")

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    #clear tsaging table before each run
    cursor.execute("TRUNCATE TABLE stg_transactions")

    insert_query = """
        INSERT INTO stg_transactions (
            transaction_id, customer_id, transaction_date, amount,
            transaction_type, channel, category, status, 
            merchant_name, balance_after     
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    records = df[[
        "transaction_id","customer_id","transaction_date","amount",
        "transaction_type","channel","category","status",
        "merchant_name","balance_after"
    ]].values.tolist()

    #Replace Python None/NaN safely
    records = [
        [None if (isinstance(v,float) and pd.isna(v)) else v for v in row]
        for row in records
    ]

    cursor.executemany(insert_query, records)
    conn.commit()

    print(f"  {cursor.rowcount} records loaded into stg_transactions")

    cursor.close()
    conn.close()

    return df # pass to TRANSFORM step
