import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

host = os.getenv('MONGO_HOST')
port = os.getenv('MONGO_PORT')

url = f"mongodb://{host}:{port}"

client = MongoClient(url)
