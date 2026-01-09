from fastapi import FastAPI, Depends
from typing import Annotated

from app.dependencies import check_coupon_validity, select_category, time_range
from app.middleware import ClientInfoMiddleware

app = FastAPI()

app.add_middleware(ClientInfoMiddleware)

@app.get("/v1/trips")
def get_tours(
    time_range: Annotated[time_range, Depends()],
):
    start, end = time_range
    message = f"Request trips from {start}"
    if end:
        return f"{message} to {end}"
    return message

@app.get("/v2/trips/{category}")
def get_trips_by_category(
    category: Annotated[select_category, Depends()],
    discount_applicable: Annotated[
        bool, Depends(check_coupon_validity)
    ],
):
    category = category.replace("-", " ").title()
    message = f"You requested {category} trips."

    if discount_applicable:
        message += (
            "\n. The coupon code is valid! "
            "You will get a discount!"
        )
    return message


