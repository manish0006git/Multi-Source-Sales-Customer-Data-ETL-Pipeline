"""Extracts raw sales data from a source relational database."""

import pandas as pd
from sqlalchemy.engine import Engine


def extract_db(engine: Engine, table_name: str) -> pd.DataFrame:
    """
    Read an entire table from the source database into a DataFrame.

    Args:
        engine: SQLAlchemy engine connected to the source database.
        table_name: Name of the table to extract.

    Returns:
        DataFrame containing the table's rows. Returns an empty DataFrame
        if the table does not exist yet (useful for first-time/demo runs).
    """
    try:
        df = pd.read_sql_table(table_name, con=engine)
    except ValueError:
        # Table doesn't exist yet — expected on a fresh demo environment
        df = pd.DataFrame()
    return df
