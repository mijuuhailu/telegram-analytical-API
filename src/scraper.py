from telethon import TelegramClient
from telegram_client import client
from config import PHONE_NUMBER


# async def main():
#     # Connect to Telegram
#     await client.start(phone=PHONE_NUMBER)

#     print("Successfully connected to Telegram!")

#     # Display your own account information
#     me = await client.get_me()

#     print(f"Logged in as: {me.first_name}")
#     print(f"Username: {me.username}")
#     print(f"Phone: {me.phone}")

async def main():
    await client.start(phone=PHONE_NUMBER)

    channel = "@chemed123"   

    async for message in client.iter_messages(channel, limit=5):
        print("------------------------")
        print("ID:", message.id)
        print("Date:", message.date)
        print("Text:", message.text)


with client:
    client.loop.run_until_complete(main())