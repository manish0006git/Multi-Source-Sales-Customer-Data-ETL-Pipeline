"""
Main ETL pipeline orchestrator.

Usage:
    python -m src.pipeline
    python -m src.pipeline --config config/config.yaml --verbose
"""

import argparse
import time

import yaml
from dotenv import load_dotenv

from src.extract.csv_extractor import extract_csv
from src.extract.api_extractor import extract_api
from src.extract.db_extractor import extract_db
from src.transform.cleaner import clean_data
from src.transform.enrichment import add_revenue_column, add_date_parts
from src.transform.validator import validate_schema, validate_row_count, ValidationError
from src.load.warehouse_loader import load_to_warehouse
from src.utils.logger import get_logger
from src.utils.db_connector import get_engine


def load_config(config_path: str) -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def run_pipeline(config_path: str = "config/config.yaml", verbose: bool = False) -> None:
    load_dotenv()
    config = load_config(config_path)

    log_level = "DEBUG" if verbose else config.get("logging", {}).get("level", "INFO")
    logger = get_logger(
        __name__,
        log_dir=config["logging"]["log_dir"],
        log_file=config["logging"]["log_file"],
        level=log_level,
    )

    start_time = time.time()

    # ---- EXTRACT ----
    logger.info("Starting EXTRACT stage")
    csv_df = extract_csv(config["extract"]["csv"]["input_path"])
    logger.info(f"  CSV source: {len(csv_df)} rows")

    try:
        api_df = extract_api(
            config["extract"]["api"]["endpoint_env_var"],
            config["extract"]["api"]["timeout_seconds"],
        )
        logger.info(f"  API source: {len(api_df)} rows")
    except Exception as e:
        logger.warning(f"  API extraction skipped/failed: {e}")

    source_engine = get_engine("SOURCE_DB_URI")
    db_df = extract_db(source_engine, config["extract"]["database"]["source_table"])
    logger.info(f"  DB source: {len(db_df)} rows")

    # Combine primary sales data (CSV is treated as the primary sales feed here;
    # extend this to a real union/merge once your DB/API shapes are finalized)
    combined_df = csv_df.copy()
    logger.info(f"Extract stage complete — {len(combined_df)} total rows")

    # ---- TRANSFORM ----
    logger.info("Starting TRANSFORM stage")
    before_count = len(combined_df)

    cleaned_df = clean_data(
        combined_df,
        required_columns=config["transform"]["required_columns"],
        drop_duplicates=config["transform"]["drop_duplicates"],
        null_strategy=config["transform"]["null_strategy"],
    )

    try:
        validate_schema(cleaned_df, config["transform"]["required_columns"])
        validate_row_count(cleaned_df, min_rows=1)
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        raise

    enriched_df = add_revenue_column(cleaned_df)
    enriched_df = add_date_parts(enriched_df)

    after_count = len(enriched_df)
    logger.info(
        f"Transform stage complete — {after_count} rows after cleaning "
        f"({before_count - after_count} dropped)"
    )

    # ---- LOAD ----
    logger.info("Starting LOAD stage")
    warehouse_engine = get_engine("WAREHOUSE_DB_URI")
    row_counts = load_to_warehouse(
        enriched_df,
        warehouse_engine,
        fact_table=config["load"]["warehouse"]["fact_table"],
        if_exists=config["load"]["warehouse"]["if_exists"],
    )
    summary = " | ".join(f"{k}: {v}" for k, v in row_counts.items())
    logger.info(f"Load stage complete — {summary}")

    elapsed = time.time() - start_time
    logger.info(f"Pipeline finished in {elapsed:.2f}s")


def main():
    parser = argparse.ArgumentParser(description="Run the ETL pipeline")
    parser.add_argument("--config", default="config/config.yaml", help="Path to config YAML")
    parser.add_argument("--verbose", action="store_true", help="Enable DEBUG logging")
    args = parser.parse_args()

    run_pipeline(config_path=args.config, verbose=args.verbose)


if __name__ == "__main__":
    main()
