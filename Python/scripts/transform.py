import pandas as pd

def transform(df):
    print("\n [TRANSFORM] Cleaning and Validating data...")
    initial_count = len(df)
    rejected = []


    #----1. Strip Whitespaces from all string colums ---
    df = df.apply(lambda col: col.str.strip() if col.dtype=="object" else col)
    print(" Stripped Whitespaces ")


    #---2. Standardize Casing ---
    for col in ["transaction_type","channel","category","status"]:
        df[col] = df[col].str.upper()
    print("  Standardized Casing")


    #---3. Drop rows with null critical feilds ---
    before = len(df)
    null_mask = df["customer_id"].isna() | df["transaction_id"].isna() | df["amount"].isna()
    rejected_df = df[null_mask].copy()
    rejected_df["rejection_reason"] = "Null in Critical Field"
    rejected.append(rejected_df)
    df = df[~null_mask]
    print(f"  Dropped {before - len(df)} rows with critical feilds")


    #---4. Convert and validate amount ---
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    invalid_amount = df["amount"].isna()
    rejected_df2 = df[invalid_amount].copy()
    rejected_df2["rejection_reason"] = "Invalid amount"
    rejected.append(rejected_df2)
    df = df[~invalid_amount]
    print("  Validated amount column")


    #---5. Convert transaction_date to datetime ---
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    invalid_dates = df["transaction_date"].isna()
    rejected_df3 = df[invalid_dates].copy()
    rejected_df3["rejection_reason"]="Invalid date" 
    rejected.append(rejected_df3)
    df = df[~invalid_dates]
    print("  Validated transaction_date Column")


    #---6. Validate Status Values ---
    valid_statuses = ["SUCCESS","FAILED","PENDING"]
    invalid_status = ~df["status"].isin(valid_statuses)
    rejected_df4 = df[invalid_status].copy()
    rejected_df4["rejection_reason"]="Invalid Status Values"
    rejected.append(rejected_df4)
    df = df[~invalid_status]
    print("  Validated Status Column")


    #---7. Remove Duplicates 
    before=len(df)
    df = df.drop_duplicates(subset=["transaction_id"])
    print(f"  Removed {before - len(df)} duplicate transaction IDs")


    #---8. Enrich Data ---
    df["is_large_txn"] = df["amount"].abs() > 50000
    df["txn_month"] = df["transaction_date"].dt.strftime("%Y-%m")
    df["balance_after"] = pd.to_numeric(df["balance_after"], errors="coerce")
    print("  Enriched: added is_large_txn  and txn_month columns")

    #---Summary---
    total_rejected = sum(len(r) for r in rejected)
    print(f"\n  Transform Summary:")
    print(f"  records in: {initial_count}")
    print(f"  records rejected: {total_rejected}")
    print(f"  records clean: {len(df)}")

    return df, total_rejected

