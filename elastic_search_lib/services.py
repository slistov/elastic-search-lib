from typing import List

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk


class ElasticProvider:
    __es: AsyncElasticsearch

    def __init__(
        self,
        elastic_uri,
        username,
        password,
        verify_certs=True
    ) -> None:
        self.__es = AsyncElasticsearch(
            elastic_uri,
            basic_auth=(username, password),
            verify_certs=verify_certs
        )

    async def add_index(self, index, mappings, settings):
        await self.__es.indices.create(
            index=index,
            mappings=mappings,
            settings=settings
        )

    async def get_index_by_name(self, index):
        return await self.__es.indices.get(index=index)

    async def add_docs_bulk(self, index, docs_bulk):
        try:
            result = await async_bulk(self.__es, docs_bulk, index=index)
            return result
        except Exception:
            return False

    async def search(self, text, fields: List[str], index='index-default'):
        query = {
            "multi_match": {
                "query": text,
                "fields": fields
            }
        }
        response = await self.__es.search(index=index, query=query)
        return response
