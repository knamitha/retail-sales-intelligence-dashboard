import pandas as pd
import os

RAW_DATA_PATH = "retail_project/data/superstore.csv"

def extract_data(path=RAW_DATA_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Could not find {path}")
    df = pd.read_csv(path, encoding="latin1")
    print(f"[EXTRACT] Loaded {len(df)} rows, {len(df.columns)} columns.")
    return df
