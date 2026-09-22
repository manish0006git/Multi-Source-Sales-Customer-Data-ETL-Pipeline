"""Cleaning routines: null handling, duplicate removal, type standardization."""

import pandas as pd


def clean_data(df: pd.DataFrame, required_columns: list, drop_duplicates: bool = True,
               null_strategy: str = "drop") -> pd.DataFrame:
    """
    Apply standard cleaning steps to a raw DataFrame.

    Args:
        df: Raw input DataFrame.
        required_columns: Columns that must be present and non-null.
        drop_duplicates: Whether to drop exact duplicate rows.
        null_strategy: How to handle nulls in required_columns —
                        "drop" (remove rows), "fill_zero", or "fill_mean".

    Returns:
        Cleaned DataFrame.
    """
    if df.empty:
        return df

    cleaned = df.copy()

    # Keep only columns that actually exist to avoid KeyErrors on partial sources
    present_required = [c for c in required_columns if c in cleaned.columns]

    if drop_duplicates:
        cleaned = cleaned.drop_duplicates()

    if null_strategy == "drop":
        cleaned = cleaned.dropna(subset=present_required)
    elif null_strategy == "fill_zero":
        cleaned[present_required] = cleaned[present_required].fillna(0)
    elif null_strategy == "fill_mean":
        for col in present_required:
            if pd.api.types.is_numeric_dtype(cleaned[col]):
                cleaned[col] = cleaned[col].fillna(cleaned[col].mean())

    # Standardize date columns if present
    if "transaction_date" in cleaned.columns:
        cleaned["transaction_date"] = pd.to_datetime(
            cleaned["transaction_date"], errors="coerce"
        )
        cleaned = cleaned.dropna(subset=["transaction_date"])

    # Standardize numeric columns
    for col in ("quantity", "unit_price"):
        if col in cleaned.columns:
            cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    cleaned = cleaned.dropna(subset=[c for c in ("quantity", "unit_price") if c in cleaned.columns])

    return cleaned.reset_index(drop=True)
