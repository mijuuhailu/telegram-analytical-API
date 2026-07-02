from pathlib import Path
import json

from telethon import TelegramClient
from telegram_client import client
from config import PHONE_NUMBER

import asyncio
import logging
from datetime import datetime

from telethon.errors import FloodWaitError




CHANNELS = {
    "CheMed123": 100,
    "lobelia4cosmetics": 100,
    "TIKVAHPHARMA": 100,
}


# =====================================================
# Logging Configuration
# =====================================================

Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


# =====================================================
# Download Image
# =====================================================

async def download_image(message, channel_name):
    """
    Download the image from a Telegram message.
    Returns the image path or None.
    """

    if not message.photo:
        return None

    image_dir = Path("../data/raw/images") / channel_name
    image_dir.mkdir(parents=True, exist_ok=True)

    image_path = image_dir / f"{message.id}.jpg"

    await client.download_media(
        message,
        file=image_path
    )

    return str(image_path)


# =====================================================
# Scrape One Channel
# =====================================================

async def scrape_channel(channel_name, limit=100):
    """
    Scrape all messages from a Telegram channel.
    """

    logger.info(f"Scraping channel: {channel_name}")

    messages = []

    async for message in client.iter_messages(channel_name, limit=limit):

        try:

            image_path = await download_image(
                message,
                channel_name
            )

            # Preserve original Telegram structure
            raw_message = message.to_dict()

            # Add our own metadata
            raw_message["channel_name"] = channel_name
            raw_message["image_path"] = image_path
            raw_message["scraped_at"] = datetime.now().isoformat()
            

            messages.append(raw_message)

        except FloodWaitError as e:

            logger.warning(
                f"Rate limit reached. Waiting {e.seconds} seconds..."
            )

            await asyncio.sleep(e.seconds)

        except Exception as e:

            logger.exception(
                f"Failed to process message {message.id}: {e}"
            )

    logger.info(
        f"{channel_name}: {len(messages)} messages scraped."
    )

    return messages


# =====================================================
# Save JSON
# =====================================================

def save_json(channel_name, messages):
    """
    Save scraped messages into the partitioned data lake.
    """

    scrape_date = datetime.now().strftime("%Y-%m-%d")

    output_dir = (
        Path("../data/raw/telegram_messages")
        / scrape_date
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = output_dir / f"{channel_name}.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            messages,
            f,
            indent=4,
            ensure_ascii=False,
            default=str
        )

    logger.info(
        f"Saved {len(messages)} messages to {output_file}"
    )


# =====================================================
# Main
# =====================================================

async def main():

    logger.info("Connecting to Telegram...")

    await client.start(phone=PHONE_NUMBER)

    logger.info("Successfully connected.")

    for channel_name, limit in CHANNELS.items():

        try:

            messages = await scrape_channel(channel_name, limit=limit)
            save_json(channel_name, messages)

        except Exception as e:

            logger.exception(
                f"Error scraping {channel_name}: {e}"
            )

    logger.info("Scraping completed.")


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":

    with client:
        client.loop.run_until_complete(main())