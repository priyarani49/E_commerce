
# -----------------------------------------
# E-COMMERCE SALES DATA ANALYSIS
# -----------------------------------------

# Step 1: Import required libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Step 2: Read the Excel dataset

df = pd.read_excel("Ecommerce_Sales_Dataset.xlsx")


# Step 3: Display basic information

print("\n----- FIRST 5 RECORDS -----")
print(df.head())

print("\n----- DATASET INFORMATION -----")
print(df.info())

print("\n----- DATASET SIZE -----")
print(df.shape)

print("\n----- COLUMN NAMES -----")
print(df.columns)

print("\n----- MISSING VALUES -----")
print(df.isnull().sum())


# Step 4: Basic sales analysis

print("\n----- SALES ANALYSIS -----")

total_sales = df["Sales (INR)"].sum()
total_profit = df["Profit (INR)"].sum()
total_quantity = df["Quantity"].sum()
total_orders = df["Order ID"].nunique()

print("Total Sales: Rs.", total_sales)
print("Total Profit: Rs.", total_profit)
print("Total Quantity Sold:", total_quantity)
print("Total Orders:", total_orders)

print("\nAverage Sales:", df["Sales (INR)"].mean())
print("Average Profit:", df["Profit (INR)"].mean())


# Step 5: Category-wise sales

print("\n----- CATEGORY WISE SALES -----")

category_sales = df.groupby("Category")["Sales (INR)"].sum()

print(category_sales)


# Step 6: Region-wise sales

print("\n----- REGION WISE SALES -----")

region_sales = df.groupby("Region")["Sales (INR)"].sum()

print(region_sales)


# Step 7: Top 5 selling products

print("\n----- TOP 5 PRODUCTS -----")

top_products = df.groupby("Product Name")["Quantity"].sum()

top_products = top_products.sort_values(ascending=False)

print(top_products.head(5))


# Step 8: Monthly sales analysis

df["Order Date"] = pd.to_datetime(df["Order Date"])

df["Month"] = df["Order Date"].dt.month

monthly_sales = df.groupby("Month")["Sales (INR)"].sum()

print("\n----- MONTHLY SALES -----")
print(monthly_sales)


# -----------------------------------------
# DATA VISUALIZATION
# -----------------------------------------

sns.set_style("whitegrid")


# GRAPH 1: BAR CHART - Category-wise Sales

plt.figure(figsize=(8, 5))

category_sales.plot(kind="bar")

plt.title("Category-wise Sales")
plt.xlabel("Product Category")
plt.ylabel("Total Sales (INR)")

plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# GRAPH 2: LINE CHART - Monthly Sales

plt.figure(figsize=(8, 5))

monthly_sales.plot(kind="line", marker="o")

plt.title("Monthly Sales Analysis")
plt.xlabel("Month")
plt.ylabel("Total Sales (INR)")

plt.xticks(range(1, 13))
plt.grid(True)
plt.tight_layout()
plt.show()


# GRAPH 3: PIE CHART - Payment Method

payment_count = df["Payment Method"].value_counts()

plt.figure(figsize=(7, 7))

plt.pie(
    payment_count,
    labels=payment_count.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Sales Orders by Payment Method")
plt.tight_layout()
plt.show()


# GRAPH 4: HISTOGRAM - Sales Distribution

plt.figure(figsize=(8, 5))

plt.hist(df["Sales (INR)"], bins=20, edgecolor="black")

plt.title("Distribution of Sales")
plt.xlabel("Sales Amount (INR)")
plt.ylabel("Number of Orders")

plt.tight_layout()
plt.show()


# GRAPH 5: SCATTER PLOT - Sales vs Profit

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="Sales (INR)",
    y="Profit (INR)"
)

plt.title("Sales vs Profit Analysis")
plt.xlabel("Sales (INR)")
plt.ylabel("Profit (INR)")

plt.tight_layout()
plt.show()


# GRAPH 6: BAR CHART - Region-wise Profit

region_profit = df.groupby("Region")["Profit (INR)"].sum()

plt.figure(figsize=(8, 5))

region_profit.plot(kind="bar")

plt.title("Region-wise Profit Analysis")
plt.xlabel("Region")
plt.ylabel("Total Profit (INR)")

plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# GRAPH 7: COUNT PLOT - Order Status

plt.figure(figsize=(8, 5))

sns.countplot(data=df, x="Order Status")

plt.title("Order Status Analysis")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")

plt.xticks(rotation=15)
plt.tight_layout()
plt.show()


print("\nSales Analysis Completed Successfully!")
