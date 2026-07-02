# Telegram Medical Data Platform

## Overview

This project is an end-to-end data engineering pipeline that collects, processes, enriches, and exposes analytical insights from public Ethiopian medical Telegram channels.

The pipeline extracts Telegram messages and images, stores them in a raw data lake, transforms the data into a PostgreSQL data warehouse using dbt, enriches image data with YOLO object detection, exposes analytics through a FastAPI application, and orchestrates the workflow using Dagster.

## Technologies

* Python
* Telethon
* PostgreSQL
* dbt
* YOLOv8 (Ultralytics)
* FastAPI
* SQLAlchemy
* Dagster

## Project Structure

```
telegram-analytical-API/
│
├── api/                    # FastAPI application
├── data/
│   ├── raw/
│   │   ├── images/
│   │   └── telegram_messages/
│   └── yolo_results.csv
├── logs/
├── medical_warehouse/      # dbt project
├── src/                    # Scraper, loader and YOLO scripts
├── pipeline.py             # Dagster pipeline
├── schedule.py             # Dagster schedule
├── requirements.txt
└── README.md
```

## Pipeline Workflow

1. Scrape messages and images from Telegram channels.
2. Store raw JSON files and images in the data lake.
3. Load raw data into PostgreSQL.
4. Transform the data into a star schema using dbt.
5. Enrich image data using YOLO object detection.
6. Expose analytical endpoints with FastAPI.
7. Automate the pipeline using Dagster.

## Data Warehouse

### Raw Layer

* `raw.telegram_messages`
* `raw.yolo_detections`

### Staging Layer

* `stg_telegram_messages`

### Mart Layer

* `dim_channels`
* `dim_dates`
* `fct_messages`
* `fct_image_detections`

## API Endpoints

* `GET /api/reports/top-products`
* `GET /api/channels/{channel_name}/activity`
* `GET /api/search/messages`
* `GET /api/reports/visual-content`

API documentation is available at:

```
http://localhost:8000/docs
```

## Running the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Scrape Telegram data

```bash
python src/scraper.py
```

### 3. Load data into PostgreSQL

```bash
python src/load_to_postgres.py
```

### 4. Run dbt transformations

```bash
cd medical_warehouse
dbt run
dbt test
```

### 5. Run YOLO detection

```bash
python src/yolo_detect.py
```

### 6. Start the API

```bash
uvicorn api.main:app --reload
```

### 7. Run the pipeline

```bash
dagster dev -f pipeline.py
```

## Features

* Telegram data scraping
* Raw data lake storage
* PostgreSQL data warehouse
* Star schema dimensional modeling
* dbt transformations and data quality tests
* YOLO image enrichment
* FastAPI analytical API
* Dagster pipeline orchestration

## Author

Developed as part of a Data Engineering project for building an analytical data platform using modern ELT and machine learning techniques.
