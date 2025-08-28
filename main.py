from flask import request
import pandas as pd
import mysql.connector

# The point of this app is to take sales data and return re-order points for each item





def forecast_moving_avg(sales_data, window_size=7, lead_time_days=2, safety_stock=0):
    """
    Calculate sales forecast based on moving average of daily sales.
    
    Parameters:
    sales_data (DataFrame): DataFrame containing 'item_id', 'date' and 'quantity_sold' columns.
    window_size (int): Number of days to consider for moving average.
    lead_time_days (int): Lead time in days to receive new stock.
    safety_stock (int): Additional stock to prevent stockouts.
    
    Returns:
    DataFrame: DataFrame with 'item_id' and 'reorder_point' columns.
    """
    # Calculate daily sales
    sales_data['daily_sales'] = sales_data.groupby('item_id')['quantity_sold'].transform(lambda x: x.rolling(window=window_size, min_periods=1).mean())
    
    # Calculate reorder point
    sales_data['reorder_point'] = (sales_data['daily_sales'] * lead_time_days) + safety_stock
    
    return sales_data[['item_id', 'reorder_point']]

def safety_stock_std_dev(sales_data, lead_time_days=2, service_level=1.65):
    """
    Calculate safety stock based on standard deviation of daily sales.
    
    Parameters:
    sales_data (DataFrame): DataFrame containing 'item_id', 'date' and 'quantity_sold' columns.
    lead_time_days (int): Lead time in days to receive new stock.
    service_level (float): Z-score corresponding to desired service level (e.g., 1.65 for 95%).
    
    Returns:
    DataFrame: DataFrame with 'item_id' and 'safety_stock' columns.
    """

    # Calculate standard deviation of daily sales
    std_dev = sales_data.groupby('item_id')['daily_sales'].std().reset_index()
    std_dev.columns = ['item_id', 'std_dev_daily_sales']
    
    # Calculate safety stock
    std_dev['safety_stock'] = std_dev['std_dev_daily_sales'] * (lead_time_days ** 0.5) * service_level
    
    return std_dev[['item_id', 'safety_stock']]


# Connect to MySQL database
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="DSA6cux2",
    database="mydb"
)


