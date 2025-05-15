from fastapi import FastAPI
from routes.PracticeRoutes import router as practice_router
from routes.previewRoutes import router as preview_router
from routes.user_routes import router as user_router
from routes.rolRoutes import router as rolRouter
from routes.emailRoutes import router as emailRouter
from routes.documentRequestRoutes import router as document_request_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Gestión de Prácticas API")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(practice_router)
app.include_router(preview_router)
app.include_router(user_router)
app.include_router(rolRouter)
app.include_router(emailRouter)
app.include_router(document_request_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
