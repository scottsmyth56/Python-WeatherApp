import os
from dotenv import load_dotenv

load_dotenv()

#USER = os.environ.get("DB_USER")
#PASSWORD = os.environ.get("DB_PASSWORD")
#PORT = os.environ.get("DB_PORT")
HOST = os.environ.get("DATABASE_URL")
#NAME = os.environ.get("DB_NAME")
API_KEY = os.environ.get("API_KEY")
