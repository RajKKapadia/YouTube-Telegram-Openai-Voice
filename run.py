from fastapi import FastAPI

from app import router

app = FastAPI()

app.include_router(router)
