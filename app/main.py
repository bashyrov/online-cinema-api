from fastapi import FastAPI
from app.routers.online_cinema import router as online_cinema_router
app = FastAPI()
app.include_router(online_cinema_router)

