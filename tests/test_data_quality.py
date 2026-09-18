from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "retail_sales_clean.csv"

REQUIRED_COLUMNS = {
    "Order_ID","Order_Date","Customer_ID","Customer_Name","Product_ID",
    "Product_Name","Category","Region","City","Quantity","Unit_Price",
    "Discount","Revenue","Cost","Profit","Payment_Method","Customer_Segment",
    "Year","Month","Month_Name","Quarter","Profit_Margin_Pct"
}

def load_data():
    return pd.read_csv(DATA)

def test_required_columns_exist():
    df = load_data()
    assert REQUIRED_COLUMNS.issubset(df.columns)

def test_order_ids_are_unique():
    df = load_data()
    assert df["Order_ID"].is_unique

def test_no_missing_values():
    df = load_data()
    assert not df.isna().any().any()

def test_positive_quantities_and_prices():
    df = load_data()
    assert (df["Quantity"] > 0).all()
    assert (df["Unit_Price"] > 0).all()

def test_revenue_profit_relationship():
    df = load_data()
    delta = (df["Revenue"] - df["Cost"] - df["Profit"]).abs()
    assert (delta < 0.02).all()

def test_discount_range():
    df = load_data()
    assert df["Discount"].between(0, 1).all()
