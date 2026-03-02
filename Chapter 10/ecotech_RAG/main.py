from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, Request
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import Chroma

from typing import Annotated
from model import chain
from documents import load_documents, get_context

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Chroma(
        embedding_function=CohereEmbeddings(model="embed-english-v3.0")
    )
    await load_documents(db)
    yield {"db": db}

app = FastAPI(
    title="Ecotech AI Assistant",
    lifespan=lifespan
)

@app.post("/message")
async def query_assistant(
    request: Request,
    question: Annotated[str, Body()],
) -> str:
    context = get_context(question, request.state.db)
    response = await chain.ainvoke(
        {
            "question": question,
            "context": context,
        }
    )
    return response



