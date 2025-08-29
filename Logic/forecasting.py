import pandas as pd

# --- 1) Date parsing ---------------------------------------------------------
def coerce_dates(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """Return a copy with date_col parsed; handles Excel serials and strings."""
    out = df.copy()
    s = out[date_col]
    if pd.api.types.is_numeric_dtype(s):
        out[date_col] = pd.to_datetime(s, origin="1899-12-30", unit="D", errors="coerce")
    else:
        out[date_col] = pd.to_datetime(s, errors="coerce")
    return out.dropna(subset=[date_col])

# --- 2) (Optional) sales coercion (keep if you might get strings like '1,234') ---
def coerce_sales_numeric(df: pd.DataFrame, sales_col: str) -> pd.DataFrame:
    """Return a copy with sales_col coerced to numeric; drops non-numeric rows."""
    out = df.copy()
    s = (
        out[sales_col].astype(str)
                       .str.replace('\u00A0', '', regex=False)  # NBSP
                       .str.replace(' ', '', regex=False)
                       .str.replace(',', '.', regex=False)
                       .str.replace(r'[^\d\.\-]', '', regex=True)
    )
    out[sales_col] = pd.to_numeric(s, errors='coerce')
    return out.dropna(subset=[sales_col])

# --- 3) Summarize per item ---------------------------------------------------
def summarize_items(df: pd.DataFrame, item_col: str, date_col: str, sales_col: str) -> pd.DataFrame:
    """Return per-item first/last date, totals, active days, and calendar duration."""
    g = (df.groupby(item_col, as_index=False)
           .agg(first_date=(date_col, 'min'),
                last_date=(date_col,  'max'),
                total_sales=(sales_col, 'sum'),
                active_days=(date_col, 'nunique')))
    g['duration_days'] = (g['last_date'] - g['first_date']).dt.days + 1
    return g

def productSalesStdev(sales_data: pd.DataFrame, item_col: str = 'item_id', sales_col: str = 'quantity_sold', date_col: str = 'date') -> pd.DataFrame:
    """
    Return: [item, sales_stdev]
    """
    df = sales_data[[item_col, date_col, sales_col]]
    df = coerce_dates(df, date_col)
    df = coerce_sales_numeric(df, sales_col)

    # Compute the standard deviation of sales per item
    stdev = df.groupby(item_col)[sales_col].std().reset_index()
    stdev.columns = [item_col, 'sales_stdev']
    return stdev