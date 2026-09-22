Multi-Source Sales & Customer Data ETL Pipeline
A production-style ETL (Extract, Transform, Load) pipeline built in Python that consolidates sales data from multiple sources — CSV files, a REST API, and a source database — cleans and validates it, and loads it into a star-schema data warehouse for analytics.

Python License Tests Docker

📌 Overview
This project simulates a real-world data engineering workflow:

Extract raw data from three heterogeneous sources (CSV, public API, SQLite source DB)
Transform it — clean nulls/duplicates, standardize types, enrich with derived fields, validate against a schema
Load it into a star-schema warehouse (fact_sales, dim_customer, dim_product, dim_date)
Log every stage's row counts, durations, and errors
Test each stage with pytest
Containerize with Docker for one-command reproducibility
CI via GitHub Actions — lint + test on every push
🏗️ Architecture
 ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
 │  CSV Files  │     │  REST API   │     │ Source DB   │
 └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                             ▼
                    ┌─────────────────┐
                    │   EXTRACT       │
                    │ (raw DataFrames)│
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │  TRANSFORM      │
                    │ clean/validate/ │
                    │ enrich          │
                    └────────┬────────┘
                             ▼
                    ┌─────────────────┐
                    │    LOAD         │
                    │ star-schema DW  │
                    │  (SQLite/PG)    │
                    └─────────────────┘
📂 Project Structure
etl-pipeline-project/
├── src/
│   ├── extract/        # Source-specific extractors (CSV, API, DB)
│   ├── transform/       # Cleaning, validation, enrichment logic
│   ├── load/            # Warehouse loader (star schema)
│   ├── utils/           # Logger, DB connector helpers
│   └── pipeline.py      # Orchestrates the full ETL run
├── config/
│   └── config.yaml      # Paths, DB URIs, API endpoints
├── data/
│   ├── raw/              # Extracted raw data lands here
│   ├── processed/        # Transformed data lands here
│   └── sample_data.csv   # Sample input for demo runs
├── tests/                # pytest unit tests per stage
├── logs/                 # Pipeline run logs
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .github/workflows/ci.yml
⚙️ Setup
Option A — Local (virtualenv)
git clone https://github.com/<your-username>/etl-pipeline-project.git
cd etl-pipeline-project
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # fill in any secrets/config overrides

# Optional: seed a demo source database so the DB-extraction path has data
python scripts/seed_source_db.py
Option B — Docker
docker-compose up --build
This spins up the pipeline in a container with all dependencies pre-installed.

▶️ Running the Pipeline
python -m src.pipeline
Optional flags:

python -m src.pipeline --config config/config.yaml --verbose
Expected console output:

[INFO] Extract stage complete — 3 sources, 12,480 rows
[INFO] Transform stage complete — 12,110 rows after cleaning (370 dropped)
[INFO] Load stage complete — fact_sales: 12,110 | dim_customer: 843 | dim_product: 216
[INFO] Pipeline finished in 4.32s
🧪 Running Tests
pytest tests/ -v
🗃️ Data Model (Star Schema)
Table	Type	Description
fact_sales	Fact	One row per transaction — quantity, price, customer_id, product_id, date_id
dim_customer	Dimension	Customer attributes
dim_product	Dimension	Product attributes
dim_date	Dimension	Date breakdown (day/month/year/quarter)
🔧 Configuration
All paths, database URIs, and API endpoints live in config/config.yaml — nothing is hardcoded in the source. Secrets (API keys, DB passwords) are read from .env (see .env.example).

🚀 Future Improvements
Orchestrate with Apache Airflow (DAG scheduling, retries, backfills)
Stream ingestion with Kafka for near-real-time loads
Deploy warehouse to PostgreSQL/Redshift in the cloud
Add Great Expectations for data quality gates
Incremental/CDC loading instead of full refresh
📄 License
MIT License — free to use and adapt.

👤 Author
Manish Bawa
— B.E. Computer Engineering, aspiring Data Engineer.
