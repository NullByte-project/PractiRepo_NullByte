from fastapi import FastAPI

app = FastAPI(title="PRACTIREPO", description="Repositorio de practicas", version="1.0.0")

@app.get("/", tags=["Main"])
def main():
    return {"message": "Welcome to PractiRepo"}