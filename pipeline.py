from dagster import job, op, Nothing, In
import subprocess


from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

@op
def scrape_telegram_data():
    subprocess.run(
        ["python", "src/scraper.py"],
        cwd=PROJECT_ROOT,
        check=True
    )


@op(ins={"start": In(Nothing)})
def load_raw_to_postgres():
    subprocess.run(["python", "src/load_to_postgres.py"], check=True)


@op(ins={"start": In(Nothing)})
def run_dbt_transformations():
    subprocess.run(["dbt", "run"], cwd="medical_warehouse", check=True)


@op(ins={"start": In(Nothing)})
def run_yolo_enrichment():
    subprocess.run(["python", "src/yolo_detect.py"], check=True)


@job
def telegram_pipeline():
    scrape = scrape_telegram_data()
    load = load_raw_to_postgres(scrape)
    dbt = run_dbt_transformations(load)
    run_yolo_enrichment(dbt)