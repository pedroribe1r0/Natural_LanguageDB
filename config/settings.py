import os
from dotenv import load_dotenv

load_dotenv(override=True)

def get_db_data():
    return os.getenv("DB_USERNAME"), os.getenv("DB_PASSWORD"),  os.getenv("DB_HOST"), int(os.getenv("DB_PORT", 3306))

def get_api_key():
    return os.getenv("GOOGLE_API_KEY")