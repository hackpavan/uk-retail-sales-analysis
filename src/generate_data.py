import random
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
random.seed(SEED)
rng = np.random.default_rng(SEED)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "raw" / "retail_sales.csv"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

N_ORDERS = 20_000
N_CUSTOMERS = 1_000

regions = {
    "London": ["London"],
    "South East": ["Brighton", "Oxford", "Reading", "Southampton"],
    "South West": ["Bristol", "Plymouth", "Exeter"],
    "East of England": ["Cambridge", "Norwich", "Ipswich"],
    "West Midlands": ["Birmingham", "Coventry", "Wolverhampton"],
    "East Midlands": ["Nottingham", "Leicester", "Derby"],
    "North West": ["Manchester", "Liverpool", "Preston"],
    "North East": ["Newcastle", "Sunderland", "Middlesbrough"],
    "Yorkshire": ["Leeds", "Sheffield", "York"],
    "Wales": ["Cardiff", "Swansea", "Newport"],
    "Scotland": ["Edinburgh", "Glasgow", "Aberdeen"],
    "Northern Ireland": ["Belfast", "Derry"],
}

region_weights = {
    "London": 0.19, "South East": 0.13, "South West": 0.07,
    "East of England": 0.08, "West Midlands": 0.09, "East Midlands": 0.07,
    "North West": 0.11, "North East": 0.05, "Yorkshire": 0.08,
    "Wales": 0.05, "Scotland": 0.06, "Northern Ireland": 0.02
}

products = [
    ("P001", "Laptop Pro 14", "Electronics", 999, 720),
    ("P002", "Laptop Air 13", "Electronics", 799, 560),
    ("P003", "Wireless Headphones", "Electronics", 149, 85),
    ("P004", "Bluetooth Speaker", "Electronics", 89, 48),
    ("P005", "Mechanical Keyboard", "Electronics", 119, 65),
    ("P006", "Wireless Mouse", "Electronics", 49, 24),
    ("P007", "4K Monitor", "Electronics", 399, 255),
    ("P008", "USB-C Hub", "Electronics", 59, 29),
    ("P009", "Office Chair", "Furniture", 249, 145),
    ("P010", "Standing Desk", "Furniture", 499, 310),
    ("P011", "Desk Lamp", "Furniture", 69, 32),
    ("P012", "Bookshelf", "Furniture", 179, 105),
    ("P013", "Filing Cabinet", "Furniture", 139, 82),
    ("P014", "Office Desk", "Furniture", 329, 195),
    ("P015", "Running Shoes", "Sports", 119, 65),
    ("P016", "Training Shoes", "Sports", 99, 53),
    ("P017", "Yoga Mat", "Sports", 39, 18),
    ("P018", "Dumbbell Set", "Sports", 79, 43),
    ("P019", "Fitness Tracker", "Sports", 129, 72),
    ("P020", "Sports Backpack", "Sports", 59, 31),
    ("P021", "Coffee Machine", "Home Appliances", 199, 115),
    ("P022", "Air Fryer", "Home Appliances", 129, 70),
    ("P023", "Robot Vacuum", "Home Appliances", 349, 220),
    ("P024", "Electric Kettle", "Home Appliances", 49, 25),
    ("P025", "Toaster", "Home Appliances", 39, 20),
    ("P026", "Blender", "Home Appliances", 69, 35),
    ("P027", "Backpack", "Accessories", 79, 38),
    ("P028", "Leather Wallet", "Accessories", 59, 25),
    ("P029", "Travel Bag", "Accessories", 109, 52),
    ("P030", "Smart Watch", "Accessories", 229, 135),
]
prod_df = pd.DataFrame(products, columns=["Product_ID","Product_Name","Category","Base_Price","Base_Cost"])

category_weights = {
    "Electronics": 0.31,
    "Furniture": 0.18,
    "Sports": 0.18,
    "Home Appliances": 0.20,
    "Accessories": 0.13,
}
category_to_products = {
    c: prod_df[prod_df["Category"] == c].reset_index(drop=True)
    for c in category_weights
}

first_names = [
    "James","Oliver","George","Harry","Jack","Jacob","Noah","Charlie","Muhammad","Thomas",
    "Emily","Olivia","Amelia","Isla","Ava","Isabella","Mia","Sophia","Grace","Ella",
    "Liam","Ethan","Lucas","Mason","Leo","Freya","Lily","Sophie","Evie","Chloe"
]
last_names = [
    "Smith","Jones","Taylor","Brown","Wilson","Davies","Evans","Thomas","Johnson","Roberts",
    "Walker","Wright","Thompson","White","Hughes","Edwards","Green","Hall","Clarke","Lewis"
]

customers = []
for i in range(1, N_CUSTOMERS + 1):
    segment = random.choices(["Consumer", "Small Business", "Corporate"], weights=[65,25,10], k=1)[0]
    customers.append({
        "Customer_ID": f"C{i:04d}",
        "Customer_Name": f"{random.choice(first_names)} {random.choice(last_names)}",
        "Customer_Segment": segment
    })
customers_df = pd.DataFrame(customers)

dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
month_weight = {1:0.85,2:0.82,3:0.92,4:0.95,5:1.00,6:1.02,7:1.05,8:1.00,9:1.08,10:1.12,11:1.32,12:1.48}
date_probs = np.array([month_weight[d.month] for d in dates], dtype=float)
date_probs /= date_probs.sum()

region_list = list(region_weights)
region_probs = np.array([region_weights[r] for r in region_list], dtype=float)
region_probs /= region_probs.sum()

category_list = list(category_weights)
category_probs = np.array([category_weights[c] for c in category_list], dtype=float)
category_probs /= category_probs.sum()

rows = []
for i in range(1, N_ORDERS + 1):
    order_date = pd.Timestamp(rng.choice(dates.to_numpy(), p=date_probs))
    cust = customers_df.iloc[rng.integers(0, N_CUSTOMERS)]
    region = rng.choice(region_list, p=region_probs)
    city = random.choice(regions[region])
    category = rng.choice(category_list, p=category_probs)
    cpdf = category_to_products[category]
    prod = cpdf.iloc[rng.integers(0, len(cpdf))]

    unit_price = round(max(5, prod["Base_Price"] * rng.normal(1.0, 0.025)), 2)
    unit_cost = round(prod["Base_Cost"] * rng.normal(1.0, 0.015), 2)

    if cust["Customer_Segment"] == "Corporate":
        qty = random.choices([1,2,3,4,5,6,8,10], weights=[20,24,20,14,9,6,4,3], k=1)[0]
    elif cust["Customer_Segment"] == "Small Business":
        qty = random.choices([1,2,3,4,5,6], weights=[35,28,18,10,6,3], k=1)[0]
    else:
        qty = random.choices([1,2,3,4,5], weights=[58,24,10,6,2], k=1)[0]

    discount_choices = [0, 0.05, 0.10, 0.15, 0.20]
    discount_w = [25,27,25,15,8] if order_date.month in [11,12] else [47,25,17,8,3]
    if cust["Customer_Segment"] == "Corporate":
        discount_w = [max(1, discount_w[0]-8), discount_w[1]+3, discount_w[2]+3, discount_w[3]+1, discount_w[4]+1]
    discount = random.choices(discount_choices, weights=discount_w, k=1)[0]

    revenue = round(unit_price * qty * (1 - discount), 2)
    cost = round(unit_cost * qty, 2)
    profit = round(revenue - cost, 2)

    rows.append({
        "Order_ID": f"ORD{i:06d}",
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Customer_ID": cust["Customer_ID"],
        "Customer_Name": cust["Customer_Name"],
        "Product_ID": prod["Product_ID"],
        "Product_Name": prod["Product_Name"],
        "Category": category,
        "Region": region,
        "City": city,
        "Quantity": int(qty),
        "Unit_Price": unit_price,
        "Discount": discount,
        "Revenue": revenue,
        "Cost": cost,
        "Profit": profit,
        "Payment_Method": random.choices(
            ["Credit Card","Debit Card","PayPal","Bank Transfer"],
            weights=[44,35,16,5], k=1
        )[0],
        "Customer_Segment": cust["Customer_Segment"],
    })

df = pd.DataFrame(rows)

# Add a few raw-data quality issues so the cleaning stage has meaningful work.
for idx in rng.choice(df.index, size=60, replace=False):
    df.loc[idx, "City"] = np.nan
for idx in rng.choice(df.index, size=40, replace=False):
    df.loc[idx, "Payment_Method"] = np.nan
for idx in rng.choice(df.index, size=50, replace=False):
    df.loc[idx, "Customer_Name"] = str(df.loc[idx, "Customer_Name"]) + "  "

df = pd.concat([df, df.sample(80, random_state=SEED)], ignore_index=True)
df.to_csv(OUTPUT, index=False)

print(f"Created {len(df):,} raw rows at {OUTPUT}")
print("The raw file includes a small number of duplicates/missing values intentionally for cleaning practice.")
