from fastapi import Depends, HTTPException
from typing import Optional
from fastapi import APIRouter

router = APIRouter()

VALID_API_KEYS = [
    "a",
    "b",
    "c",
]


async def get_api_key(
    api_key: Optional[str],
):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key.",
        )
    return api_key

@router.get("/secure-data")
async def get_secure_data(
    api_key: str = Depends(get_api_key),
):
    return {
        "message": "Access to secure data granted",
    }
