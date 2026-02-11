from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import Body, FastAPI, Request
from handlers import generate_chat_completion

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield {"messages": []}

app = FastAPI(
    title="Chef cuisine chatbot app",
    lifespan=lifespan,
)

@app.post("/query")
async def query_chat_bot(
    request: Request,
    query: Annotated[str, Body(min_length=1)],
) -> str:
    answer = await  generate_chat_completion(
        query, request.state.messages
    )
    return answer

