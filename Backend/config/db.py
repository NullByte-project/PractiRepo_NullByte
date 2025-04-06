from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Cargar variables del .env
load_dotenv()

# Obtener la URI desde el entorno
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Conectarse a MongoDB
conn = MongoClient(MONGO_URI, server_api=ServerApi('1'))

try:
    conn.admin.command('ping')
    print("Conexión realizada correctamente")
except Exception as e:
    print("Error al conectar con MongoDB:", e)

# 🔹 Base de datos a usar (desde .env)
db = conn[DATABASE_NAME]