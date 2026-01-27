from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class GRPCResponse(BaseModel):
    message: str
    received: bool

grpc_channel = grpc.aio.insecure_channel(
    "localhost:50051"
)

@app.get()