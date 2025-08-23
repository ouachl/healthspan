import pandas as pd
import mysql.connector

# Read CSV file into DataFrame
def read_csv(path: str, encoding: str="utf-8") -> pd.DataFrame:
    return pd.read_csv(path, encoding=encoding)

# Check if a table exists in the database
def table_exists(db_connection: mysql.connector.MySQLConnection, table_name: str) -> bool:
    # Return True if a table exists in the connected database
    cur = db_connection.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM information_schema.tables "
        "WHERE table_schema = DATABASE() AND table_name = %s",
        (table_name,)
    )
    exists = cur.fetchone()[0] > 0
    cur.close()
    return exists

# Append DataFrame to MySQL table
def append_df_to_ventes(df, db_connection, table_name: str="ventes"):
    if not table_exists(db_connection, table_name):
        raise ValueError(f"Table '{table_name}' does not exist in the database.")
        
    # NaN -> None for MySQL
    df = df.where(pd.notnull(df), None)

    # Prepare SQL query
    cols = list(df.columns)
    col_sql = ", ".join(f"`{c}`" for c in cols)
    placeholders = ", ".join(["%s"] * len(cols))
    sql = f"INSERT INTO `{table_name}` ({col_sql}) VALUES ({placeholders})"

    # Convert DataFrame to list of tuples
    rows = [tuple(row) for row in df.itertuples(index=False, name=None)]

    # Execute the query
    cursor = db_connection.cursor()
    try:
        cursor.executemany(sql, rows)
        db_connection.commit()
        return cursor.rowcount
    finally:
        cursor.close()


# ----------------------------
# Main Program Logic
# ----------------------------

# Connect to MySQL database
with mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="DSA6cux2",
    database="mydb"
) as db_connection:

    leDF = read_csv("/Users/laythouach/Desktop/ventes.csv")
    try:
        inserted_rows = append_df_to_ventes(df=leDF, db_connection=db_connection, table_name="ventes")
        print(f"Inserted rows: {inserted_rows}")
    except ValueError as e:
        print(e)
    except mysql.connector.Error as db_err:
        print(f"Database error: {db_err}")