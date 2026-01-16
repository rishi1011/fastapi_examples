import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, WebSocketException, status

from app.chat import router as chat_router

app = FastAPI()
app.include_router(chat_router)

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
                logger.warning("Disconnetinggg...")
                return await websocket.close(
                    code=status.WS_1000_NORMAL_CLOSURE,
                    reason="Disconnecting..."
                )
            if "bad message" in data:
                raise WebSocketException(
                    code=status.WS_1008_POLICY_VIOLATION,
                    reason="Inappropriate message"
                )
                
    except WebSocketDisconnect as e:
        logger.warning(
            f"Connection closed by the client (code={e.code})"
        )
    
