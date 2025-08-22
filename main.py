import pandas as pd
import sqlite3

# Connect to a database (creates it if it doesn't exist)
conn = sqlite3.connect('mydatabase.db')

# Extract sales data from CSV file in array
def extract_sales_data(sales_data):
    return pd.read_csv(sales_data).to_numpy()

# Calculate total sales from the extracted data
def calculate_total_sales(sales_data, sales_column='sales'):
    return extract_sales_data(sales_data).sum()

