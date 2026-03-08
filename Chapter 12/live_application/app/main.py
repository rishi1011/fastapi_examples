from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI(title="FastAPI Live Application")

app.add_middleware(HTTPSRedirectMiddleware)

@app.get("/")
def read_root():
    return {"Hello": "World"}

