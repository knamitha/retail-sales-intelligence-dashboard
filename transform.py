import pandas as pd
import numpy as np

def find_column(df, possible_names):
    for name in possible_names:
        for col in df.columns:
            if col.strip().lower() == name.strip().lower():
                return col
    return None

def clean_data(df):
    col_map = {
        "order_date": find_column(df, ["Order Date"]),
        "product_name": find_column(df, ["Product Name"]),
        "category": find_column(df, ["Category"]),
        "sub_category": find_column(df, ["Sub-Category", "Sub Category"]),
        "customer_name": find_column(df, ["Customer Name"]),
        "segment": find_column(df, ["Segment"]),
        "region": find_column(df, ["Region"]),
        "state": find_column(df, ["State"]),
        "city": find_column(df, ["City"]),
        "sales_amount": find_column(df, ["Sales"]),
    }

    missing = [k for k, v in col_map.items() if v is None]
    if missing:
        raise KeyError(f"Required columns missing: {missing}")

    df = df.rename(columns={v: k for k, v in col_map.items()})
    required_cols = list(col_map.keys())
    df = df[required_cols].copy()

    df = df.dropna(subset=["order_date", "product_name", "customer_name"])
    df = df.drop_duplicates()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])
    df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors="coerce").fillna(0)

    # This dataset version has no Quantity/Profit columns, so we estimate
    # reasonable values for demonstration purposes:
    np.random.seed(42)
    df["quantity"] = np.random.randint(1, 8, size=len(df))
    df["profit"] = (df["sales_amount"] * np.random.uniform(0.05, 0.35, size=len(df))).round(2)

    print(f"[TRANSFORM] Final cleaned row count: {len(df)}")
    print("[TRANSFORM] Note: Quantity and Profit were estimated since the source file didn't include them.")
    return df

def build_dim_date(df):
    dates = df["order_date"].drop_duplicates().sort_values().reset_index(drop=True)
    dim_date = pd.DataFrame({"full_date": dates})
    dim_date["day"] = dim_date["full_date"].dt.day
    dim_date["month"] = dim_date["full_date"].dt.month
    dim_date["month_name"] = dim_date["full_date"].dt.strftime("%B")
    dim_date["quarter"] = dim_date["full_date"].dt.quarter
    dim_date["year"] = dim_date["full_date"].dt.year
    return dim_date

def build_dim_product(df):
    return df[["product_name", "category", "sub_category"]].drop_duplicates().reset_index(drop=True)

def build_dim_customer(df):
    return df[["customer_name", "segment"]].drop_duplicates().reset_index(drop=True)

def build_dim_region(df):
    return df[["region", "state", "city"]].drop_duplicates().reset_index(drop=True)

def transform_all(raw_df):
    clean_df = clean_data(raw_df)
    dim_date = build_dim_date(clean_df)
    dim_product = build_dim_product(clean_df)
    dim_customer = build_dim_customer(clean_df)
    dim_region = build_dim_region(clean_df)
    return clean_df, dim_date, dim_product, dim_customer, dim_region
