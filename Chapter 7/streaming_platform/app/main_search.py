import json
import logging

from fastapi import APIRouter, Depends, HTTPException
from elasticsearch import BadRequestError
from fastapi_cache.decorator import cache

from app.db_connection import es_client
from app.es_queries import (
    top_ten_artists_query,
)

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/search", tags=["search"])

def get_elasticsearch_client():
    return es_client

@router.get("/top/ten/artists/{country}")
async def top_ten_artist_by_country(
    country: str,
    es_client = Depends(get_elasticsearch_client),
):
    try: 
        response = await es_client.search(
            **top_ten_artists_query(country)
        )
    except BadRequestError as e:
        logger.error(e)

        raise HTTPException(
            status_code=400,
            detail="Invalid country"
        )
    
    return [
        {
            "artist": record.get("key"),
            "views": record.get("views", {}).get(
                "value"
            ),
        }
        for record in response["aggregations"]["top_ten_artists"]["buckets"]
    ]