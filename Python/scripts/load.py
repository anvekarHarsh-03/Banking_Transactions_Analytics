import pandas as pd
import mysql.connector
from config import DB_CONFIG

def load(df, records_extracted, recoreds_rejected):
    print("\n [LOAD] Loading clean data inot fact_transactions ...")

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO fact_transactions (
            transaction_id, customer_id, transaction_date, amount,
            transaction_type, channel, category, status,
            merchant_name, balance_after, is_large_txn, txn_month    
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
            status = VALUES(status),
            balance_after = VALUES(balance_after),
            loaded_at = CURRENT_TIMESTAMP
    """

    records = []
    for _, row in df.iterrows():
        #Skip rows where date is still NaT
        if pd.isnull(row["transaction_date"]):
            continue
        records.append((
            row["transaction_id"],
            row["customer_id"],
            row["transaction_date"].strftime("%Y-%m-%d %H:%M:%S"),
            float(row["amount"]),
            row["transaction_type"],
            row["channel"],
            row["category"],
            row["status"],
            row["merchant_name"],
            float(row["balance_after"]) if row["balance_after"] == row["balance_after"] else None,
            bool(row["is_large_txn"]),
            row["txn_month"] 
        ))

    cursor.executemany(insert_query,records)
    conn.commit()
    records_loaded = cursor.rowcount
    print("  {records_loaded} records loaded into fact_transactions")


    #---Write to audit log---
    cursor.execute("""
        INSERT INTO etl_audit_log (records_extracted, records_rejected, records_loaded, status, notes)    
        VALUES(%s,%s,%s,%s,%s)    
    """,(
        records_extracted,
        recoreds_rejected,
        records_loaded,
        "SUCCESS",
        "pipeline ran sucessfully"
    ))
    conn.commit()
    print("  Aduit log updated")

    cursor.close()
    conn.close()