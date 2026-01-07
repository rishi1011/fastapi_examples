from app.db_connection import es_client
from songs_info import songs_info
from elasticsearch import AsyncElasticsearch

mapping = {
    "mappings": {
        "properties": {
            "artist": {"type": "keyword"},
            "views_per_country": {
                "type": "object",
                "dynamic": True,
            },
        }
    }
}


async def fill_elastichsearch():
    for song in songs_info:
        await es_client.index(index="songs_index", body=song)
    await es_client.close()


async def create_index():
    await es_client.options(
        request_timeout=30, ignore_status=[400, 404]
    ).indices.create(
        index="songs_index",
        body=mapping,
    )
    await es_client.close()


async def delete_all_indexes():
    await es_client.options(ignore_status=[400, 404]).indices.delete(index="*")
    await es_client.close()


async def main():
    async with AsyncElasticsearch(
        "http://localhost:9200",
        request_timeout=30,
    ) as es:
        await delete_all_indexes()
        await create_index()
        await fill_elastichsearch()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
