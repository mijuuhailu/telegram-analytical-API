# Telegram Data Scraping and Collection

## Objective

Build a data collection pipeline that extracts messages and images from public Telegram channels and stores them in a raw data lake for later processing.

## What Was Implemented

* Connected to the Telegram API using **Telethon**.
* Scraped messages from public Telegram channels.
* Extracted raw message data while preserving the original Telegram API structure.
* Downloaded images from messages containing photos.
* Stored images in a structured directory:

  ```
  data/raw/images/{channel_name}/{message_id}.jpg
  ```
* Stored raw message data as JSON files using a date-partitioned data lake structure:

  ```
  data/raw/telegram_messages/YYYY-MM-DD/{channel_name}.json
  ```
* Implemented logging to record scraping activities and errors.
* Added error handling, including Telegram rate-limit (`FloodWaitError`) handling.

## Project Structure

```
medical-data-platform/
│
├── data/
│   └── raw/
│       ├── images/
│       └── telegram_messages/
│
├── logs/
│   └── scraper.log
│
├── src/
│   ├── config.py
│   ├── telegram_client.py
│   └── scraper.py
│
├── .env
├── .gitignore
└── requirements.txt
```

## Technologies Used

* Python
* Telethon
* python-dotenv
* JSON
* Logging

## Output

After running the scraper:

* Raw Telegram messages are stored as JSON files.
* Images are downloaded and organized by channel.
* Scraping logs are written to `logs/scraper.log`.

This raw data serves as the input for **Task 2**, where it will be loaded into PostgreSQL and transformed into a dimensional data warehouse using dbt.
