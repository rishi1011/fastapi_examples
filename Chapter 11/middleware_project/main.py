import logging

from fastapi import Body, FastAPI
from starlette.middleware import Middleware
from middleware.asgi_middleware import ASGIMiddleware
from middleware.request_middleware import HashBodyContentMiddleWare

logger = logging.getLogger("uvicorn")

app = FastAPI(
    title="Middleware Application",
    middleware=[
        Middleware(
            ASGIMiddleware,
            parameter="example parameter",
        ),
    ]
)

app.add_middleware(
    HashBodyContentMiddleWare,
    allowed_paths=["/send"],
)

@app.get("/")
async def read_root():
    return {"Hello": "Middleware World"}

@app.post("/send")
async def send(message: str = Body()):
    logger.info(f"Message: {message}")
    return message