import asyncio
import time
from contextlib import contextmanager
from multiprocessing import Process

import uvicorn
from httpx import AsyncClient

from app.main import app
from app.profiler import ProfileEndpointsMiddleware
from app.internationalization import router

def run_server():
    app.add_middleware(ProfileEndpointsMiddleware)
    uvicorn.run(app, port=8000)

@contextmanager
def run_server_in_process():
    p = Process(target=run_server)
    p.start()
    time.sleep(2)
    yield
    p.terminate()

async def make_requests(n: int):
    async with AsyncClient(
        base_url="http://localhost:8000"
    ) as client:
        tasks = (
            client.get(
                "/homepage", timeout=float("inf"), headers={"Accept-Language": "fr_FR"}
            )
            for _ in range(n)
        )
        responses = await asyncio.gather(*tasks)

        for i, response in enumerate(responses, start=1):
            print(f"Response {i}:")
            print("Status:", response.status_code)
            print("Body:", response.json())


async def main():
    with run_server_in_process():
        print("Server is running in a seperate process")
        await make_requests(2)

if __name__ == "__main__":
    asyncio.run(main())
