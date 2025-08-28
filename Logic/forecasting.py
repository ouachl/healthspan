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

# --- 4) Compute averages ------------------------------------------------------
def add_avg_daily_sales(summary: pd.DataFrame, duration_mode: str = 'active') -> pd.DataFrame:
    """Add avg_daily_sales using chosen denominator ('active' or 'calendar')."""
    out = summary.copy()
    if duration_mode == 'active':
        denom = out['active_days']
    elif duration_mode == 'calendar':
        denom = out['duration_days']
    else:
        raise ValueError("duration_mode must be 'active' or 'calendar'")
    out['avg_daily_sales'] = out['total_sales'] / denom.clip(lower=1)
    return out

# --- 5) Thin wrapper ----------------------------------------------------------
def forecast_avg_sales(
    sales_data: pd.DataFrame,
    item_col: str = 'item_id',
    sales_col: str = 'quantity_sold',
    date_col: str = 'date',
    duration_mode: str = 'active'
) -> pd.DataFrame:
    """
    Return: [item, total_sales, duration_days, active_days, avg_daily_sales]
    """
    df = sales_data[[item_col, date_col, sales_col]]
    df = coerce_dates(df, date_col)
    # Keep this line if your sales column might be non-numeric; otherwise remove it.
    # df = coerce_sales_numeric(df, sales_col)

    summary = summarize_items(df, item_col, date_col, sales_col)
    result  = add_avg_daily_sales(summary, duration_mode)
    return result[[item_col, 'total_sales', 'duration_days', 'active_days', 'avg_daily_sales']]




# Example usage:
item_col = str("Libelle")
sales_col = str("Qte vendue")
date_col = str("Date")

file = "/Users/laythouach/Desktop/sales_data.csv"
sales_data_df = pd.read_csv(file)
print(forecast_avg_sales(sales_data_df, item_col, sales_col, date_col))