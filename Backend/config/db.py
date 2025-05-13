# config/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Cargar las variables del entorno
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
print(MONGO_URI)

DB_NAME = os.getenv("DATABASE_NAME", "repositorio_practicas")
print(DB_NAME)

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
print(BREVO_API_KEY)

# Cliente asíncrono motor
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
