import logging

from os import getpid

from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI(title="FastAPI Live Application")

# app.add_middleware(HTTPSRedirectMiddleware)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")   

@app.get("/")
def read_root():
    logger.info(f"Processed by worker {getpid()}")
    return {"Hello": "World"}

