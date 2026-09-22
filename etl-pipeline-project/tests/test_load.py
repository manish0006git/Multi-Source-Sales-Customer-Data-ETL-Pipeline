"""Unit tests for the load stage."""

import pandas as pd
from sqlalchemy import create_engine, inspect

from src.load.warehouse_loader import (
    build_dim_customer,
    build_dim_product,
    build_dim_date,
    build_fact_sales,
    load_to_warehouse,
)


def make_transformed_df():
    return pd.DataFrame({
        "transaction_id": [1, 2],
        "customer_id": ["C001", "C002"],
        "customer_name": ["Aarav", "Priya"],
        "customer_region": ["West", "South"],
        "product_id": ["P001", "P002"],
        "product_name": ["Mouse", "Chair"],
        "category": ["Electronics", "Furniture"],
        "transaction_date": pd.to_datetime(["2026-01-01", "2026-01-02"]),
        "year": [2026, 2026],
        "month": [1, 1],
        "day": [1, 2],
        "quarter": [1, 1],
        "quantity": [2, 1],
        "unit_price": [499.0, 3499.0],
        "revenue": [998.0, 3499.0],
    })


def test_build_dim_customer_deduplicates():
    df = make_transformed_df()
    dim = build_dim_customer(df)
    assert len(dim) == 2
    assert set(dim.columns) == {"customer_id", "customer_name", "customer_region"}


def test_build_fact_sales_selects_expected_columns():
    df = make_transformed_df()
    fact = build_fact_sales(df)
    assert "revenue" in fact.columns
    assert "customer_name" not in fact.columns


def test_load_to_warehouse_writes_tables():
    df = make_transformed_df()
    engine = create_engine("sqlite:///:memory:")

    row_counts = load_to_warehouse(df, engine, fact_table="fact_sales", if_exists="replace")

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    assert "fact_sales" in tables
    assert "dim_customer" in tables
    assert "dim_product" in tables
    assert "dim_date" in tables
    assert row_counts["fact_sales"] == 2
