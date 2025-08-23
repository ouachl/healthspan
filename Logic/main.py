import pandas as pd
import mysql.connector

# Connect to MySQL database
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="DSA6cux2",
    database="mydb"
)

cursor = connection.cursor()

# Example query to fetch data from a table
cursor.execute("SELECT * FROM customers")
rows = cursor.fetchall()
for row in rows:
    print(row, "\n")

cursor.close()
connection.close()

# Extract sales data from CSV file in array
def extract_sales_data(sales_data):
    return pd.read_csv(sales_data).to_numpy()

# Calculate total sales from the extracted data
def calculate_total_sales(sales_data, sales_column='sales'):
    return extract_sales_data(sales_data).sum()

