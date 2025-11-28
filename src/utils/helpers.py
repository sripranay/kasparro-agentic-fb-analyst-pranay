# src/utils/helpers.py
from typing import Tuple, Dict
import pandas as pd
import numpy as np


def compute_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute common advertising KPIs and return a dataframe with new columns:
      - ctr (clicks / impressions)
      - cpc (spend / clicks)  [NaN if clicks == 0]
      - cpa (spend / purchases) [NaN if purchases == 0]
      - roas (revenue / spend) [NaN if spend == 0]

    Expects numeric columns: spend, impressions, clicks, purchases, revenue
    """
    df = df.copy()

    # Safely coerce numeric fields
    for col in ["spend", "impressions", "clicks", "purchases", "revenue"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        else:
            df[col] = np.nan

    # CTR
    df["ctr"] = np.where(
        df["impressions"].fillna(0) > 0,
        df["clicks"].fillna(0) / df["impressions"].fillna(1),
        np.nan,
    )

    # CPC
    df["cpc"] = np.where(df["clicks"].fillna(0) > 0, df["spend"] / df["clicks"], np.nan)

    # CPA
    df["cpa"] = np.where(
        df["purchases"].fillna(0) > 0, df["spend"] / df["purchases"], np.nan
    )

    # ROAS
    df["roas"] = np.where(df["spend"].fillna(0) > 0, df["revenue"] / df["spend"], np.nan)

    return df


def summarize_df(df: pd.DataFrame) -> Dict[str, dict]:
    """
    Produce simple summary statistics per column similar to pandas.describe()
    but returns a dict of dicts for easy JSON-serialization.
    Only numeric columns will have mean/std/min/max; object columns get counts & top.
    """
    summary = {}
    for col in df.columns:
        series = df[col]
        if pd.api.types.is_numeric_dtype(series):
            summary[col] = {
                "count": int(series.count()),
                "mean": None if series.count() == 0 else float(series.mean()),
                "std": None if series.count() == 0 else float(series.std()),
                "min": None if series.count() == 0 else float(series.min()),
                "25%": None,
                "50%": None if series.count() == 0 else float(series.median()),
                "75%": None,
                "max": None if series.count() == 0 else float(series.max()),
            }
        else:
            # treat as categorical/text
            top = None
            freq = None
            if series.count() > 0:
                top = series.dropna().astype(str).mode().iloc[0] if not series.dropna().empty else None
                freq = int(series.dropna().astype(str).value_counts().get(top, 0)) if top else None
            summary[col] = {
                "count": int(series.count()),
                "unique": int(series.nunique(dropna=True)),
                "top": top,
                "freq": freq,
            }
    return summary


def split_windows(
    df: pd.DataFrame, date_col: str = "date", recent_days: int = 7, prev_days: int = 7
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split dataset into two windows based on the latest date in `date_col`:
      - recent window: last `recent_days`
      - previous window: the `prev_days` immediately before the recent window

    Returns: (recent_df, previous_df)
    Expects date_col to be parseable by pandas.to_datetime.
    """
    if date_col not in df.columns:
        raise ValueError(f"Date column '{date_col}' not found in DataFrame")

    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])
    df = df.sort_values(by=date_col)

    last_date = df[date_col].max()
    if pd.isna(last_date):
        return pd.DataFrame(), pd.DataFrame()

    recent_start = last_date - pd.Timedelta(days=recent_days - 1)
    prev_end = recent_start - pd.Timedelta(days=1)
    prev_start = prev_end - pd.Timedelta(days=prev_days - 1)

    recent_df = df[df[date_col] >= recent_start]
    prev_df = df[(df[date_col] >= prev_start) & (df[date_col] <= prev_end)]

    return recent_df, prev_df


def percent_change(a: float, b: float) -> float:
    """
    Compute percentage change from b -> a (i.e., (a - b) / b * 100).
    Returns a float (percent). If base is zero, returns np.nan.
    """
    try:
        a = float(a)
        b = float(b)
    except Exception:
        return float("nan")

    if b == 0:
        return float("nan")
    return (a - b) / b * 100.0
