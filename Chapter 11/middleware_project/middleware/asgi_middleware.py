import logging 

from starlette.types import (
    ASGIApp, Scope, Receive, Send
)

logger = logging.getLogger("uvicorn")

class ASGIMiddleware:
    def __init__(self, app: ASGIApp, parameter: str = "default"):
        self.app = app
        self.parameter = parameter

    async def __call__(self, 
        scope: Scope, 
        receive: Receive, 
        send: Send,
        ):
        logger.info("Entering ASGI Middleware")
        logger.info(f"The parameter is: {self.parameter}")
        await self.app(scope, receive, send)
        logger.info("Exiting ASGI Middleware")
        
