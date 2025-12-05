from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import users

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# Conectamos el router de usuarios
# La ruta final será: POST /api/v1/users/
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])

@app.get("/")
async def root():
    return {"message": f"Bienvenido a {settings.PROJECT_NAME}"}