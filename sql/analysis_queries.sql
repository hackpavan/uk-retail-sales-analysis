USE uk_retail_analytics;

-- 1. Executive KPIs
SELECT
    ROUND(SUM(Revenue), 2) AS total_revenue,
    ROUND(SUM(Profit), 2) AS total_profit,
    COUNT(DISTINCT Order_ID) AS total_orders,
    COUNT(DISTINCT Customer_ID) AS total_customers,
    ROUND(SUM(Revenue) / COUNT(DISTINCT Order_ID), 2) AS average_order_value,
    ROUND(100 * SUM(Profit) / NULLIF(SUM(Revenue), 0), 2) AS profit_margin_pct
FROM retail_sales;

-- 2. Monthly revenue and profit trend
SELECT
    Year,
    Month,
    Month_Name,
    ROUND(SUM(Revenue), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    COUNT(DISTINCT Order_ID) AS orders
FROM retail_sales
GROUP BY Year, Month, Month_Name
ORDER BY Year, Month;

-- 3. Month-over-month revenue growth using a window function
WITH monthly_sales AS (
    SELECT
        Year,
        Month,
        SUM(Revenue) AS revenue
    FROM retail_sales
    GROUP BY Year, Month
),
with_previous AS (
    SELECT
        Year,
        Month,
        revenue,
        LAG(revenue) OVER (ORDER BY Year, Month) AS previous_month_revenue
    FROM monthly_sales
)
SELECT
    Year,
    Month,
    ROUND(revenue, 2) AS revenue,
    ROUND(previous_month_revenue, 2) AS previous_month_revenue,
    ROUND(
        100 * (revenue - previous_month_revenue) /
        NULLIF(previous_month_revenue, 0), 2
    ) AS mom_growth_pct
FROM with_previous
ORDER BY Year, Month;

-- 4. Category performance
SELECT
    Category,
    ROUND(SUM(Revenue), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(100 * SUM(Profit) / NULLIF(SUM(Revenue), 0), 2) AS profit_margin_pct,
    COUNT(DISTINCT Order_ID) AS orders
FROM retail_sales
GROUP BY Category
ORDER BY revenue DESC;

-- 5. Regional performance
SELECT
    Region,
    ROUND(SUM(Revenue), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    COUNT(DISTINCT Order_ID) AS orders,
    ROUND(SUM(Revenue) / COUNT(DISTINCT Order_ID), 2) AS average_order_value
FROM retail_sales
GROUP BY Region
ORDER BY revenue DESC;

-- 6. Top 10 products by revenue
SELECT
    Product_Name,
    Category,
    ROUND(SUM(Revenue), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    SUM(Quantity) AS units_sold
FROM retail_sales
GROUP BY Product_Name, Category
ORDER BY revenue DESC
LIMIT 10;

-- 7. Customer segment performance
SELECT
    Customer_Segment,
    ROUND(SUM(Revenue), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    COUNT(DISTINCT Customer_ID) AS customers,
    COUNT(DISTINCT Order_ID) AS orders,
    ROUND(SUM(Revenue) / COUNT(DISTINCT Customer_ID), 2) AS revenue_per_customer
FROM retail_sales
GROUP BY Customer_Segment
ORDER BY revenue DESC;

-- 8. Top customers by lifetime revenue
SELECT
    Customer_ID,
    MAX(Customer_Name) AS Customer_Name,
    MAX(Customer_Segment) AS Customer_Segment,
    COUNT(DISTINCT Order_ID) AS orders,
    ROUND(SUM(Revenue), 2) AS lifetime_revenue,
    ROUND(SUM(Profit), 2) AS lifetime_profit
FROM retail_sales
GROUP BY Customer_ID
ORDER BY lifetime_revenue DESC
LIMIT 20;

-- 9. Repeat-customer rate
WITH customer_orders AS (
    SELECT
        Customer_ID,
        COUNT(DISTINCT Order_ID) AS order_count
    FROM retail_sales
    GROUP BY Customer_ID
)
SELECT
    COUNT(*) AS customers,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(
        100.0 * SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS repeat_customer_rate_pct
FROM customer_orders;

-- 10. Discount impact
SELECT
    Discount,
    COUNT(DISTINCT Order_ID) AS orders,
    ROUND(SUM(Revenue), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(100 * SUM(Profit) / NULLIF(SUM(Revenue), 0), 2) AS profit_margin_pct
FROM retail_sales
GROUP BY Discount
ORDER BY Discount;

-- 11. Rank products within each category by revenue
WITH product_sales AS (
    SELECT
        Category,
        Product_Name,
        SUM(Revenue) AS revenue,
        SUM(Profit) AS profit
    FROM retail_sales
    GROUP BY Category, Product_Name
)
SELECT
    Category,
    Product_Name,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,
    DENSE_RANK() OVER (
        PARTITION BY Category
        ORDER BY revenue DESC
    ) AS category_revenue_rank
FROM product_sales
ORDER BY Category, category_revenue_rank;
