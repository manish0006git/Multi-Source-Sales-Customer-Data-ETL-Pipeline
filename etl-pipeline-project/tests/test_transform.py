"""Unit tests for the transform stage."""

import pandas as pd
import pytest

from src.transform.cleaner import clean_data
from src.transform.validator import (
    validate_schema,
    validate_no_negative_values,
    validate_row_count,
    ValidationError,
)
from src.transform.enrichment import add_revenue_column, add_date_parts


REQUIRED = ["transaction_id", "quantity", "unit_price", "transaction_date"]


def make_raw_df():
    return pd.DataFrame({
        "transaction_id": [1, 2, 2, 3],
        "quantity": [2, None, None, 5],
        "unit_price": [10.0, 20.0, 20.0, 15.0],
        "transaction_date": ["2026-01-01", "2026-01-02", "2026-01-02", "not-a-date"],
    })


def test_clean_data_drops_duplicates_and_nulls():
    df = make_raw_df()
    cleaned = clean_data(df, required_columns=REQUIRED, drop_duplicates=True, null_strategy="drop")

    # id=2's two duplicate rows both have a null quantity -> dropped.
    # id=3 has an invalid transaction_date -> dropped.
    # Only id=1 is fully valid and survives.
    assert len(cleaned) == 1
    assert cleaned["transaction_id"].tolist() == [1]


def test_add_revenue_column():
    df = pd.DataFrame({"quantity": [2, 3], "unit_price": [10.0, 5.0]})
    result = add_revenue_column(df)
    assert result["revenue"].tolist() == [20.0, 15.0]


def test_add_date_parts():
    df = pd.DataFrame({"transaction_date": pd.to_datetime(["2026-03-15"])})
    result = add_date_parts(df)
    assert result.loc[0, "year"] == 2026
    assert result.loc[0, "month"] == 3
    assert result.loc[0, "quarter"] == 1


def test_validate_schema_raises_on_missing_column():
    df = pd.DataFrame({"a": [1]})
    with pytest.raises(ValidationError):
        validate_schema(df, ["a", "b"])


def test_validate_no_negative_values_raises():
    df = pd.DataFrame({"quantity": [1, -2]})
    with pytest.raises(ValidationError):
        validate_no_negative_values(df, ["quantity"])


def test_validate_row_count_raises_when_empty():
    df = pd.DataFrame()
    with pytest.raises(ValidationError):
        validate_row_count(df, min_rows=1)
