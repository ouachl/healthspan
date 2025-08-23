import pandas as pd
import mysql.connector

# Connect to MySQL database
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="DSA6cux2",
    database="mydb"
)