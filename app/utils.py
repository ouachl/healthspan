import pandas as pd

def coerce_dates(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    out = df.copy()
    s = out[date_col]
    if pd.api.types.is_numeric_dtype(s):
        out[date_col] = pd.to_datetime(s, origin="1899-12-30", unit="D", errors="coerce")
    else:
        out[date_col] = pd.to_datetime(s, errors="coerce")
    return out.dropna(subset=[date_col])

def coerce_sales_numeric(df: pd.DataFrame, sales_col: str) -> pd.DataFrame:
    out = df.copy()
    s = (
        out[sales_col].astype(str)
                       .str.replace('\u00A0', '', regex=False)
                       .str.replace(' ', '', regex=False)
                       .str.replace(',', '.', regex=False)
                       .str.replace(r'[^\d\.\-]', '', regex=True)
    )
    out[sales_col] = pd.to_numeric(s, errors='coerce')
    return out.dropna(subset=[sales_col])
