from fastapi import FastAPI
from .main import router

app = FastAPI()
app.include_router(router)
