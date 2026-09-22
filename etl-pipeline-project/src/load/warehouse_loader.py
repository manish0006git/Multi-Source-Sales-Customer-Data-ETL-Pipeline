"""Loads transformed data into a star-schema data warehouse."""

import pandas as pd
from sqlalchemy.engine import Engine


def build_dim_customer(df: pd.DataFrame) -> pd.DataFrame:
    """Build a deduplicated customer dimension table from the fact data."""
    cols = [c for c in ("customer_id", "customer_name", "customer_region") if c in df.columns]
    if "customer_id" not in cols:
        return pd.DataFrame()
    return df[cols].drop_duplicates(subset=["customer_id"]).reset_index(drop=True)


def build_dim_product(df: pd.DataFrame) -> pd.DataFrame:
    """Build a deduplicated product dimension table from the fact data."""
    cols = [c for c in ("product_id", "product_name", "category") if c in df.columns]
    if "product_id" not in cols:
        return pd.DataFrame()
    return df[cols].drop_duplicates(subset=["product_id"]).reset_index(drop=True)


def build_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    """Build a deduplicated date dimension table from decomposed date parts."""
    cols = [c for c in ("transaction_date", "year", "month", "day", "quarter") if c in df.columns]
    if "transaction_date" not in cols:
        return pd.DataFrame()
    dim = df[cols].drop_duplicates(subset=["transaction_date"]).reset_index(drop=True)
    dim.insert(0, "date_id", dim.index + 1)
    return dim


def build_fact_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Select the fact-table columns from the fully transformed DataFrame."""
    cols = [c for c in (
        "transaction_id", "customer_id", "product_id", "transaction_date",
        "quantity", "unit_price", "revenue"
    ) if c in df.columns]
    return df[cols].reset_index(drop=True)


def load_to_warehouse(df: pd.DataFrame, engine: Engine, fact_table: str = "fact_sales",
                       if_exists: str = "replace") -> dict:
    """
    Split the transformed DataFrame into star-schema tables and write them
    to the warehouse database.

    Args:
        df: Fully transformed, enriched DataFrame.
        engine: SQLAlchemy engine for the target warehouse.
        fact_table: Name to give the fact table.
        if_exists: pandas.to_sql behavior — "replace" or "append".

    Returns:
        Dict of table_name -> row_count written, for logging purposes.
    """
    tables = {
        fact_table: build_fact_sales(df),
        "dim_customer": build_dim_customer(df),
        "dim_product": build_dim_product(df),
        "dim_date": build_dim_date(df),
    }

    row_counts = {}
    for table_name, table_df in tables.items():
        if table_df.empty:
            row_counts[table_name] = 0
            continue
        table_df.to_sql(table_name, con=engine, if_exists=if_exists, index=False)
        row_counts[table_name] = len(table_df)

    return row_counts
