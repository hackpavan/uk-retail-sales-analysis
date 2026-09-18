# Power BI Dashboard Build Guide

Use `data/processed/retail_sales_clean.csv` as the data source.

## Recommended one-page dashboard

### KPI cards
- Total Revenue
- Total Profit
- Profit Margin %
- Total Orders
- Average Order Value

### Visual 1 — Monthly Revenue Trend
- Visual: line chart
- Axis: Order_Date (month)
- Value: Total Revenue
- Tooltip: Total Profit, Total Orders, Revenue MoM %

### Visual 2 — Revenue by Category
- Visual: clustered bar chart
- Axis: Category
- Value: Total Revenue
- Tooltip: Total Profit, Profit Margin %

### Visual 3 — Regional Performance
- Visual: bar chart or map
- Location/Axis: Region
- Value: Total Revenue
- Tooltip: Total Profit, Average Order Value

### Visual 4 — Top Products
- Visual: horizontal bar chart
- Axis: Product_Name
- Value: Total Revenue
- Filter: Top N = 10 by Total Revenue

### Visual 5 — Customer Segments
- Visual: column chart
- Axis: Customer_Segment
- Values: Total Revenue and Total Profit

### Slicers
- Order_Date
- Region
- Category
- Customer_Segment

## Data model
This project intentionally uses a single clean fact table for simplicity.
For a more advanced version, split Product, Customer, Geography and Date into dimensions.

## Suggested title
**UK Retail Sales Performance Dashboard — 2025**

## Reference KPIs from the generated dataset
- Revenue: £7,679,530.47
- Profit: £2,625,729.03
- Orders: 20,000
- Customers: 1,000
- AOV: £383.98
- Profit margin: 34.19%

If your values differ after regenerating the dataset, check that the random seed remains `42`.
