from scripts.extract import extract
from scripts.transform import transform
from scripts.load import load 

if __name__=="__main__":
    print("=" * 50)
    print("Banking ETL Pipeline Starting...")
    print("=" * 50)

    #STEP 1: Extract
    raw_df = extract()

    #STEP 2: Transform 
    clean_df, rejected_count = transform(raw_df)

    #STEP 3: Load 
    load(clean_df, len(raw_df), rejected_count)

    print()
    print("=" * 50)
    print("  Pipleline Completed Succesfully !")
    print("=" * 50)