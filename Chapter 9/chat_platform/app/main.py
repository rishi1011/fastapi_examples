from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text(
        "Welcome to the chat room!"
    )
    await websocket.close()
    
