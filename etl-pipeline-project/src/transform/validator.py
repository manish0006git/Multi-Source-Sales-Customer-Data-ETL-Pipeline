"""Schema and data-quality validation for transformed data."""

import pandas as pd


class ValidationError(Exception):
    """Raised when a DataFrame fails required validation checks."""


def validate_schema(df: pd.DataFrame, required_columns: list) -> None:
    """
    Ensure all required columns are present in the DataFrame.

    Args:
        df: DataFrame to validate.
        required_columns: Columns that must exist.

    Raises:
        ValidationError: If any required column is missing.
    """
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValidationError(f"Missing required columns: {missing}")


def validate_no_negative_values(df: pd.DataFrame, columns: list) -> None:
    """
    Ensure the given numeric columns contain no negative values.

    Args:
        df: DataFrame to validate.
        columns: Numeric columns that should be >= 0.

    Raises:
        ValidationError: If any negative value is found.
    """
    for col in columns:
        if col in df.columns and (df[col] < 0).any():
            raise ValidationError(f"Column '{col}' contains negative values")


def validate_row_count(df: pd.DataFrame, min_rows: int = 1) -> None:
    """
    Ensure the DataFrame has at least min_rows rows.

    Args:
        df: DataFrame to validate.
        min_rows: Minimum acceptable row count.

    Raises:
        ValidationError: If row count is below the threshold.
    """
    if len(df) < min_rows:
        raise ValidationError(f"Expected at least {min_rows} rows, got {len(df)}")
