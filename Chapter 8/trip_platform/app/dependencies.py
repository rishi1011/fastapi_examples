from datetime import date, timedelta
from typing import Annotated, Tuple

from fastapi import Depends, HTTPException, Path, Query

def check_start_end_condition(start: date, end: date):
    if end and end < start:
        raise HTTPException(
            status_code=400,
            detail=(
                "End date must be "
                "greater than start date"
            ),
        )
    
def time_range(
        start: date | None = Query(
            default=date.today(),
            description=(
                "If not provided the current date is used"
            ),
            examples={"today": {"value": date.today().isoformat()}},
        ),
        end: date | None = Query(
            None,
            examples={"next week": {"value": (date.today() + timedelta(days=7)).isoformat()}},
        ),
) -> Tuple[date, date | None]:
    check_start_end_condition(start, end)
    return start, end

def select_category(
        category: Annotated[
            str,
            Path(
                description=(
                    "Kind of travel"
                    "you are interested in"
                ),
                enum=[
                    "Cruises",
                    "City Break",
                    "Resort Stay",
                ],
            ),
        ],
) -> str:
    return category

def check_coupon_validity(
        category: Annotated[select_category, Depends()],
        code: str | None = Query(
            None, description="Coupon code"
        ),
) -> bool:
    coupon_dict = {
        "cruises": "CRUISE10",
        "city-break": "CITYBREAK15",
        "resort-stay": "RESORT20",
    }

    if (
        code is not None
        and coupon_dict.get(category.lower().replace(' ', '-'), ...) == code
    ):
        return True
    return False