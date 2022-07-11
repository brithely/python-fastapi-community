from fastapi import FastAPI

from app.community.endpoints import api

app = FastAPI()

app.include_router(api.router, prefix="/api")
