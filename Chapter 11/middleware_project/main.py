import logging

from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from middleware.asgi_middleware import ASGIMiddleware
from middleware.request_middleware import HashBodyContentMiddleWare
from middleware.response_middleware import ExtraHeadersResponseMiddleware

logger = logging.getLogger("uvicorn")

app = FastAPI(
    title="Middleware Application",
    middleware=[
        Middleware(
            ASGIMiddleware,
            parameter="example parameter",
        ),
    ],
)

app.add_middleware(
    HashBodyContentMiddleWare,
    allowed_paths=["/send"],
)

app.add_middleware(
    ExtraHeadersResponseMiddleware,
    headers=(
        ("new-header", "fastapi-cookbook"),
        (
            "another-header",
            "fastapi-cookbook",
        ),
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "Middleware World"}


@app.post("/send")
async def send(message: str = Body()):
    logger.info(f"Message: {message}")
    return message
