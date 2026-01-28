from fastapi import FastAPI
from app.routers.online_cinema import router as online_cinema_router
from app.routers.auth import router as auth_router
app = FastAPI(
    root_path="/api/v1"
)
app.include_router(online_cinema_router)
app.include_router(auth_router, prefix="/auth")

