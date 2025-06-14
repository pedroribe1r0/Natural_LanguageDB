import os
from dotenv import load_dotenv

def get_db_data():
    load_dotenv()
    return os.getenv("DB_USERNAME"), os.getenv("DB_PASSWORD"),  os.getenv("DB_HOST"), int(os.getenv("DB_PORT", 3306)), os.getenv("DB_DATABASE")

def get_api_key():
    load_dotenv()
    return os.getenv("GOOGLE_API_KEY")