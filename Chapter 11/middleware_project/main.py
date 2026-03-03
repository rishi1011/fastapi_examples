from fastapi import FastAPI
from starlette.middleware import Middleware
from middleware.asgi_middleware import ASGIMiddleware

app = FastAPI(
    title="Middleware Application",
    middleware=[
        Middleware(
            ASGIMiddleware,
            parameter="example parameter",
        ),
    ]
)

@app.get("/")
async def read_root():
    return {"Hello": "Middleware World"}