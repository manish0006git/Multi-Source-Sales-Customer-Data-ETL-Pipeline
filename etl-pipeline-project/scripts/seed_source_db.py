"""
One-off helper: seeds a demo SQLite source database (data/raw/source.db)
from the sample CSV, so src/extract/db_extractor.py has something to read
on a fresh clone. Run once before your first pipeline run if you want to
exercise the DB-extraction path:

    python scripts/seed_source_db.py
"""

import pandas as pd
from sqlalchemy import create_engine

SOURCE_CSV = "data/sample_data.csv"
SOURCE_DB_URI = "sqlite:///data/raw/source.db"
TABLE_NAME = "raw_sales"


def main():
    df = pd.read_csv(SOURCE_CSV)
    engine = create_engine(SOURCE_DB_URI)
    df.to_sql(TABLE_NAME, con=engine, if_exists="replace", index=False)
    print(f"Seeded '{TABLE_NAME}' with {len(df)} rows into {SOURCE_DB_URI}")


if __name__ == "__main__":
    main()
