import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

# Validate required environment variables
if not API_ID:
    raise ValueError("API_ID environment variable is not set. Please check your .env file.")
if not API_HASH:
    raise ValueError("API_HASH environment variable is not set. Please check your .env file.")