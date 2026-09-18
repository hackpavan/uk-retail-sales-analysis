from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "retail_sales_clean.csv"

df = pd.read_csv(DATA, parse_dates=["Order_Date"])

total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()
orders = df["Order_ID"].nunique()
customers = df["Customer_ID"].nunique()
aov = total_revenue / orders
margin = total_profit / total_revenue * 100

print("UK RETAIL SALES ANALYSIS")
print("=" * 40)
print(f"Revenue: £{total_revenue:,.2f}")
print(f"Profit: £{total_profit:,.2f}")
print(f"Orders: {orders:,}")
print(f"Customers: {customers:,}")
print(f"Average order value: £{aov:,.2f}")
print(f"Profit margin: {margin:.2f}%")

print("\nTop categories")
print(df.groupby("Category")["Revenue"].sum().sort_values(ascending=False).head())

print("\nTop regions")
print(df.groupby("Region")["Revenue"].sum().sort_values(ascending=False).head())

print("\nTop products")
print(df.groupby("Product_Name")["Revenue"].sum().sort_values(ascending=False).head())
