import os
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("HOST")
user = os.getenv("USER_10T")
password = os.getenv("PASSWORD")
database = os.getenv("DB_NAME")