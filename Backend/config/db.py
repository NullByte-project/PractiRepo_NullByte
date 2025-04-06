from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Cargar variables del .env
load_dotenv()

# Obtener la URI desde el entorno
uri = os.getenv("MONGO_URI")

# Conectarse a MongoDB
conn = MongoClient(uri, server_api=ServerApi('1'))

# Verificación de conexión
try:
    conn.admin.command('ping')
    print("Conexión realizada correctamente")
except Exception as e:
    print("Error al conectar con MongoDB:", e)
