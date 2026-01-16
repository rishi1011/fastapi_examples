import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

logger = logging.getLogger("uvicorn")

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text(
        "Welcome to the chat room!"
    )
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Message received: {data}")
            await websocket.send_text("Message received!")
            if data == "disconnect":
                logger.warning("Disconneting...")
                await websocket.close()
                break
    except WebSocketDisconnect as e:
        logger.warning(
            f"Connection closed by the client (code={e.code})"
        )
    
