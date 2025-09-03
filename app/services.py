import pandas as pd
from .utils import coerce_dates, coerce_sales_numeric

REQUIRED_COLS = ["item_id", "date", "quantity_sold"]

def validate_columns(df: pd.DataFrame):
    """Ensure required columns exist, else raise error."""
    missing = [col for col in REQUIRED_COLS if col not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}. Got: {df.columns.tolist()}")


# --- 1) Average sales ---
def calculate_avg(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate average sales per item (strict columns)."""
    validate_columns(df)
    df = coerce_dates(df, "date")
    df = coerce_sales_numeric(df, "quantity_sold")

    avg = df.groupby("item_id")["quantity_sold"].mean().reset_index()
    avg.columns = ["item_id", "average_sales"]
    return avg


# --- 2) Standard deviation ---
def calculate_stdev(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate stdev of sales per item (strict columns)."""
    validate_columns(df)
    df = coerce_dates(df, "date")
    df = coerce_sales_numeric(df, "quantity_sold")

    stdev = df.groupby("item_id")["quantity_sold"].std().reset_index()
    stdev.columns = ["item_id", "sales_stdev"]
    return stdev


# --- 3) Summarize items ---
def summarize_items(df: pd.DataFrame) -> pd.DataFrame:
    """Return per-item first/last date, totals, active days, and calendar duration."""
    validate_columns(df)
    df = coerce_dates(df, "date")
    df = coerce_sales_numeric(df, "quantity_sold")

    g = (df.groupby("item_id", as_index=False)
           .agg(first_date=("date", "min"),
                last_date=("date", "max"),
                total_sales=("quantity_sold", "sum"),
                active_days=("date", "nunique")))
    g["duration_days"] = (g["last_date"] - g["first_date"]).dt.days + 1

    # convert dates to string (ISO format)
    g["first_date"] = g["first_date"].dt.strftime("%Y-%m-%d")
    g["last_date"] = g["last_date"].dt.strftime("%Y-%m-%d")

    return g



# --- 4) Product sales stdev (generic) ---
def productSalesStdev(sales_data: pd.DataFrame,
                      item_col: str = "item_id",
                      sales_col: str = "quantity_sold",
                      date_col: str = "date") -> pd.DataFrame:
    """Return per-item sales stdev."""
    df = sales_data[[item_col, date_col, sales_col]]
    df = coerce_dates(df, date_col)
    df = coerce_sales_numeric(df, sales_col)

    stdev = df.groupby(item_col)[sales_col].std().reset_index()
    stdev.columns = [item_col, "sales_stdev"]
    return stdev
