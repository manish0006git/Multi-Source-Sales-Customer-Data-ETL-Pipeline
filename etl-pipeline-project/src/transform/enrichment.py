"""Enrichment: derived columns and business-rule calculations."""

import pandas as pd


def add_revenue_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a computed 'revenue' column (quantity * unit_price).

    Args:
        df: DataFrame containing 'quantity' and 'unit_price' columns.

    Returns:
        DataFrame with an added 'revenue' column, unchanged if inputs missing.
    """
    if {"quantity", "unit_price"}.issubset(df.columns):
        df = df.copy()
        df["revenue"] = df["quantity"] * df["unit_price"]
    return df


def add_date_parts(df: pd.DataFrame, date_column: str = "transaction_date") -> pd.DataFrame:
    """
    Break a datetime column into year/month/day/quarter parts for dim_date.

    Args:
        df: DataFrame containing the date_column.
        date_column: Name of the datetime column to decompose.

    Returns:
        DataFrame with added year/month/day/quarter columns.
    """
    if date_column not in df.columns:
        return df

    df = df.copy()
    dt = pd.to_datetime(df[date_column])
    df["year"] = dt.dt.year
    df["month"] = dt.dt.month
    df["day"] = dt.dt.day
    df["quarter"] = dt.dt.quarter
    return df


def apply_currency_conversion(df: pd.DataFrame, rate: float = 1.0,
                               price_column: str = "unit_price") -> pd.DataFrame:
    """
    Convert a price column using a given exchange rate.

    Args:
        df: DataFrame containing price_column.
        rate: Conversion multiplier to apply.
        price_column: Name of the column to convert.

    Returns:
        DataFrame with the price column converted in place (copy returned).
    """
    if price_column not in df.columns or rate == 1.0:
        return df

    df = df.copy()
    df[price_column] = df[price_column] * rate
    return df
