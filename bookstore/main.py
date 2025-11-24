from endpoints import *
from models import Book

import json 

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

app.include_router(read_author.router)
app.include_router(read_book.router)
app.include_router(read_filteredBooks.router)


@app.post("/book")
async def create_book(book: Book):
    return book


class BookResponse(BaseModel):
    title: str
    author: str


@app.get("/allbooks")
async def read_all_books() -> list[BookResponse]:
    return [
        {"id": 1, "title": "1984", "author": "George Orwell"},
        {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    ]


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code, content={"message": "Oops! Something went wrong"}
    )

@app.get("/error_endpoint")
async def raise_exception():
    raise HTTPException(status_code=400)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return PlainTextResponse(
        "This is a Plain text response:"
        f"\n{json.dumps(exc.errors(), indent=2)}",
        status_code = status.HTTP_400_BAD_REQUEST,
    )