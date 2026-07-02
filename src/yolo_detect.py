import csv
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import text
from ultralytics import YOLO

from config import DB_HOST, DB_NAME, DB_USER
from db import engine

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = BASE_DIR / "data" / "raw" / "images"
OUTPUT_CSV = BASE_DIR / "data" / "yolo_results.csv"

# Load model (lightweight version)
model = YOLO(str(BASE_DIR / "src" / "yolov8n.pt"))

results_data = []

# Walk through all images
for root, dirs, files in os.walk(IMAGE_DIR):
    for file in files:
        if file.endswith((".jpg", ".png")):
            image_path = os.path.join(root, file)

            # run detection
            results = model(image_path)

            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    name = model.names[cls]
                    conf = float(box.conf[0])

                    # folder structure gives channel + message_id
                    parts = image_path.split(os.sep)
                    channel_name = parts[-2]
                    message_id = file.split(".")[0]

                    results_data.append([
                        message_id,
                        channel_name,
                        name,
                        conf,
                    ])

# Save CSV
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["message_id", "channel_name", "object", "confidence"])
    writer.writerows(results_data)

print("YOLO detection completed. Results saved to:", OUTPUT_CSV)

try:
    df = pd.read_csv(OUTPUT_CSV)

    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

    df.to_sql("yolo_detections", engine, schema="raw", if_exists="replace", index=False)
    print("Loaded YOLO results into Postgres")
except Exception as exc:
    print(f"Database upload failed: {exc}")
    print(f"Please verify your PostgreSQL credentials in .env (host={DB_HOST}, user={DB_USER}, db={DB_NAME}).")