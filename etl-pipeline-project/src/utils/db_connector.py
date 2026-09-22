"""Lightweight SQLAlchemy engine factory for source/warehouse databases."""

import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_engine(uri_env_var: str, default_uri: str = "sqlite:///data/processed/warehouse.db") -> Engine:
    """
    Build a SQLAlchemy engine from a database URI stored in an environment variable.

    Args:
        uri_env_var: Name of the environment variable holding the DB URI
                      (e.g. "SOURCE_DB_URI" or "WAREHOUSE_DB_URI").
        default_uri: Fallback URI if the environment variable is not set.

    Returns:
        A SQLAlchemy Engine instance.
    """
    uri = os.getenv(uri_env_var, default_uri)
    return create_engine(uri)
