from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "raw" / "retail_sales.csv"
OUTPUT = ROOT / "data" / "processed" / "retail_sales_clean.csv"

df = pd.read_csv(INPUT)

print(f"Raw rows: {len(df):,}")
print(f"Duplicate Order_ID values: {df['Order_ID'].duplicated().sum():,}")
print("Missing values before cleaning:")
print(df.isna().sum()[df.isna().sum() > 0])

text_cols = [
    "Customer_Name", "Product_Name", "Category", "Region",
    "City", "Payment_Method", "Customer_Segment"
]
for col in text_cols:
    df[col] = df[col].astype("string").str.strip()

df["City"] = df["City"].fillna("Unknown")
df["Payment_Method"] = df["Payment_Method"].fillna("Unknown")

df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
df = df.dropna(subset=["Order_Date"])

df = df.drop_duplicates(subset=["Order_ID"], keep="first")

numeric_cols = ["Quantity", "Unit_Price", "Discount", "Revenue", "Cost", "Profit"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=numeric_cols)
df = df[(df["Quantity"] > 0) & (df["Unit_Price"] > 0)]

df["Year"] = df["Order_Date"].dt.year
df["Month"] = df["Order_Date"].dt.month
df["Month_Name"] = df["Order_Date"].dt.strftime("%b")
df["Quarter"] = "Q" + df["Order_Date"].dt.quarter.astype(str)
df["Profit_Margin_Pct"] = np.where(
    df["Revenue"] != 0,
    df["Profit"] / df["Revenue"] * 100,
    0
)

df = df.sort_values(["Order_Date", "Order_ID"]).reset_index(drop=True)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT, index=False)

print(f"Clean rows: {len(df):,}")
print(f"Saved cleaned data to {OUTPUT}")
