from typing import List

from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.helpers import async_bulk

from ..domain import model


class ElasticProvider:
    __es: AsyncElasticsearch
    def __init__(self, es) -> None:
        self.__es = es

    async def add_index(self, index: model.Index):
        await self.__es.indices.create(index=index.index_name, mappings=index.mappings, settings=index.settings)
    
    async def get_index_by_name(self, index) -> model.Index:
        return await self.__es.indices.get(index)
    
    async def add_docs_bulk(self, index, docs_bulk):
        try:
            result = await async_bulk(self.__es, docs_bulk, index=index)
            return result
        except Exception as e:
            return False

    async def search(self, text, fields: List[str], index = 'index-default'):
        query = {
            "multi_match": {
                "query": text,
                "fields": fields
            }            
        }
        response = await self.__es.search(index=index, query=query)
        return response


async def add_doc_to_index(ep: ElasticProvider, index: str, docs_bulk):
    # Check if index exists
    try:
        await ep.get_index_by_name(index)
    # If index doesn't exist, then create
    except NotFoundError:
        index_obj = model.IndexQuote(index)
        await ep.add(index_obj)
    # Add docs bulk to index
    return await ep.add_docs_bulk(index=index, docs_bulk=docs_bulk)


async def search_index_for_text(ep: ElasticProvider, index: str, text):
    return await ep.search(index=index, text=text)