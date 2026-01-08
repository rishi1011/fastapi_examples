from datetime import date, timedelta
from typing import Tuple

from fastapi import HTTPException, Query

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