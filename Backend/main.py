from fastapi import FastAPI
from routes.user import user

app = FastAPI(title="PRACTIREPO", description="Repositorio de practicas", version="1.0.0")

app.include_router(user)

# @app.get("/", tags=["Main"])
# def main():
#     return {"message": "Welcome to PractiRepo"}