import json
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from db import engine


def serialize_nested_values(value):
    """
    Convert nested JSON-like values to JSON strings so pandas can write them
    to PostgreSQL without psycopg2 failing on dict/list objects.
    """
    if isinstance(value, (dict, list, tuple, set)):
        return json.dumps(value, ensure_ascii=False, default=str)
    return value


def prepare_dataframe_for_sql(df):
    """
    Prepare a DataFrame for SQL insertion by serializing nested values.
    """
    rows = []
    for row in df.to_dict(orient="records"):
        rows.append(
            {
                key: serialize_nested_values(value)
                for key, value in row.items()
            }
        )
    return pd.DataFrame(rows)


def create_schema():
    """
    Create the raw schema if it doesn't exist.
    """

    with engine.begin() as connection:
        connection.execute(
            text("CREATE SCHEMA IF NOT EXISTS raw;")
        )


def load_json_files():
    """
    Read all JSON files from the data lake.
    """

    json_files = Path(
        "../data/raw/telegram_messages"
    ).rglob("*.json")

    all_messages = []

    for file in json_files:

        print(f"Reading {file}")

        with open(file, "r", encoding="utf-8") as f:

            messages = json.load(f)

            all_messages.extend(messages)

    return all_messages


def load_to_postgres(messages):
    """
    Load messages into PostgreSQL.
    """

    df = pd.DataFrame(messages)
    df = prepare_dataframe_for_sql(df)

    print(f"\nLoaded {len(df)} messages.")

    print("\nColumns:")

    print(df.columns.tolist())

    df.to_sql(
        name="telegram_messages",
        con=engine,
        schema="raw",
        if_exists="replace",
        index=False,
    )

    print("\nData successfully loaded into raw.telegram_messages")


def main():

    create_schema()

    messages = load_json_files()

    load_to_postgres(messages)


if __name__ == "__main__":

    main()