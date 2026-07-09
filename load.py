import pandas as pd
from sqlalchemy import text
from retail_project.db import engine

def load_dimension(df, table_name):
    print(f"[LOAD] Loading {len(df)} rows into {table_name} ...")
    df.to_sql(table_name, engine, if_exists="append", index=False)
    with engine.connect() as conn:
        result = pd.read_sql(text(f"SELECT * FROM {table_name}"), conn)
    print(f"[LOAD] {table_name} now has {len(result)} total rows.")
    return result

def load_fact_sales(clean_df, dim_date, dim_product, dim_customer, dim_region):
    print("[LOAD] Building fact_sales rows ...")

    # Ensure both sides of the date merge are the same datetime type
    clean_df = clean_df.copy()
    dim_date = dim_date.copy()
    clean_df["order_date"] = pd.to_datetime(clean_df["order_date"])
    dim_date["full_date"] = pd.to_datetime(dim_date["full_date"])

    fact = clean_df.merge(dim_date, left_on="order_date", right_on="full_date", how="left")
    fact = fact.merge(dim_product, on=["product_name", "category", "sub_category"], how="left")
    fact = fact.merge(dim_customer, on=["customer_name", "segment"], how="left")
    fact = fact.merge(dim_region, on=["region", "state", "city"], how="left")

    fact_sales = fact[["date_id", "product_id", "customer_id", "region_id", "quantity", "sales_amount", "profit"]].copy()
    before = len(fact_sales)
    fact_sales = fact_sales.dropna(subset=["date_id", "product_id", "customer_id", "region_id"])
    print(f"[LOAD] Dropped {before - len(fact_sales)} unmatched rows.")
    fact_sales.to_sql("fact_sales", engine, if_exists="append", index=False)
    print(f"[LOAD] Loaded {len(fact_sales)} rows into fact_sales.")

def run_load(clean_df, dim_date_df, dim_product_df, dim_customer_df, dim_region_df):
    dim_date_loaded = load_dimension(dim_date_df, "dim_date")
    dim_product_loaded = load_dimension(dim_product_df, "dim_product")
    dim_customer_loaded = load_dimension(dim_customer_df, "dim_customer")
    dim_region_loaded = load_dimension(dim_region_df, "dim_region")
    load_fact_sales(clean_df, dim_date_loaded, dim_product_loaded, dim_customer_loaded, dim_region_loaded)
    print("[LOAD] Done.")
