from app.db_connection import es_client
from songs_info import songs_info

mapping = {
    "mappings": {
        "properties": {
            "artist": {
                "type": "keyword"
            },
            "views_per_country": {
                "type": "object",
                "dynamic": True,
            },
        }
    }
}

async def fill_elastichsearch():
    for song in songs_info:
        await es_client.index(
            index="songs_index", body=song
        )
    await es_client.close()