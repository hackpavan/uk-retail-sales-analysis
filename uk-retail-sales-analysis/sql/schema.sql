CREATE DATABASE IF NOT EXISTS uk_retail_analytics;
USE uk_retail_analytics;

DROP TABLE IF EXISTS retail_sales;

CREATE TABLE retail_sales (
    Order_ID VARCHAR(20) PRIMARY KEY,
    Order_Date DATE NOT NULL,
    Customer_ID VARCHAR(20) NOT NULL,
    Customer_Name VARCHAR(100) NOT NULL,
    Product_ID VARCHAR(20) NOT NULL,
    Product_Name VARCHAR(100) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    Region VARCHAR(50) NOT NULL,
    City VARCHAR(50) NOT NULL,
    Quantity INT NOT NULL,
    Unit_Price DECIMAL(10,2) NOT NULL,
    Discount DECIMAL(5,2) NOT NULL,
    Revenue DECIMAL(12,2) NOT NULL,
    Cost DECIMAL(12,2) NOT NULL,
    Profit DECIMAL(12,2) NOT NULL,
    Payment_Method VARCHAR(50) NOT NULL,
    Customer_Segment VARCHAR(50) NOT NULL,
    Year INT NOT NULL,
    Month INT NOT NULL,
    Month_Name VARCHAR(3) NOT NULL,
    Quarter VARCHAR(2) NOT NULL,
    Profit_Margin_Pct DECIMAL(8,2) NOT NULL
);
