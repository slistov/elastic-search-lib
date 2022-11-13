from ..domain import model
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.helpers import async_bulk
import abc


# class ElasticProviderAbstract(abc.ABC):
#     async def add_index(self, index: model.Index):
#         await self._add_index(self, index: model.Index):

#     @abc.abstractmethod
#     async def _add_index(self, index: model.Index):
#         raise NotImplementedError
    
#     async def get_index_by_name(self, index_name) -> model.Index:
#         return await self._get_index_by_name(self, index_name)
    
#     @abc.abstractmethod
#     async def _get_index_by_name(self, index_name) -> model.Index:
#         raise NotImplementedError

#     async def add_docs_bulk(self, index, docs_bulk):
#         return self._add_docs_bulk(self, index, docs_bulk):
    
#     @abc.abstractmethod
#     async def _add_docs_bulk(self, index, docs_bulk):
#         raise NotImplementedError

#     async def search(self, text, index = 'index-default'):
#         return self._search(self, text, index)


class ElasticProvider():
    __es: AsyncElasticsearch
    def __init__(self, es) -> None:
        self.__es = es

    async def add_index(self, index: model.Index):
        await self.__es.indices.create(index=index.index_name, mappings=index.mappings, settings=index.settings)
    
    async def get_index_by_name(self, index) -> model.Index:
        return await self.__es.indices.get(index,)
    
    async def add_docs_bulk(self, index, docs_bulk):
        try:
            result = await async_bulk(self.__es, docs_bulk, index=index)
            return result
        except Exception as e:
            return False

    async def search(self, text, index = 'index-default'):
        query = {
            "multi_match": {
                "query": text,
                "fields": ["quote^3", "movie^2", "speaker^2", "stuff*"],
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