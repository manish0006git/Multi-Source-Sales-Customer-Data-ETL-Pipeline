"""Extracts raw sales data from a CSV source file."""

import pandas as pd
from pathlib import Path


def extract_csv(input_path: str) -> pd.DataFrame:
    """
    Read a CSV file into a DataFrame.

    Args:
        input_path: Path to the source CSV file.

    Returns:
        DataFrame containing the raw CSV contents.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
    """
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV source not found at: {input_path}")

    df = pd.read_csv(path)
    return df
