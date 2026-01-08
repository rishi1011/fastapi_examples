from fastapi import FastAPI, Depends
from typing import Annotated

from app.dependencies import time_range

app = FastAPI()

@app.get("/v1/trips")
def get_tours(
    time_range: Annotated[time_range, Depends()],
):
    start, end = time_range
    print(time_range)
    print(type(time_range))
    message = f"Request trips from {start}"
    if end:
        return f"{message} to {end}"
    return message


