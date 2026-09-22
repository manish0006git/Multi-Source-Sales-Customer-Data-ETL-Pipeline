"""Unit tests for the extract stage."""

import pandas as pd
import pytest

from src.extract.csv_extractor import extract_csv


def test_extract_csv_reads_file(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("transaction_id,quantity,unit_price\n1,2,10.0\n")

    df = extract_csv(str(csv_path))

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert list(df.columns) == ["transaction_id", "quantity", "unit_price"]


def test_extract_csv_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        extract_csv("data/does_not_exist.csv")
