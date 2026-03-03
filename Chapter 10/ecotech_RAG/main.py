from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, HTTPException, Request, UploadFile
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from typing import Annotated

from langchain_text_splitters import CharacterTextSplitter
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

@app.post("/add_document")
async def add_document(
    request: Request, file: UploadFile,
):
    if file.content_type != "text/plain":
        raise HTTPException(
            status_code = 400,
            detail="File must be a text file",
        )
    
    db = request.state.db

    text_splitter = CharacterTextSplitter(
        chunk_size=100, chunk_overlap=0
    )

    content_file = file.file.read().decode()
    document = Document(content_file)

    chunks = text_splitter.split_documents(
        [document]
    )
    await db.aadd_documents(chunks)

    with open(
        f"docs/{file.filename}", "w"
    ) as buffer:
        buffer.write(content_file)

    return {
        "filename": file.filename,
    }

