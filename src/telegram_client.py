from telethon import TelegramClient
from config import API_ID, API_HASH

# Ensure API credentials are not None
assert API_ID is not None, "API_ID must be set"
assert API_HASH is not None, "API_HASH must be set"

# Create a Telegram client session
client = TelegramClient(
    "telegram_session",
    int(API_ID),
    API_HASH
)  