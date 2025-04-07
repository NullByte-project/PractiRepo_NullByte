# config/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import asyncio
import os

# Cargar variables desde .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

try:
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DATABASE_NAME]
    db.list_collection_names()
    print("Conexión exitosa")
except Exception as e:
    print(f"Error: {e}")
