import abc
from typing import List

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from ...domain import model


class ElasticIndexRepositoryAbstract(abc.ABC):
    # def __init__(self) -> None:
    #     self.docs = []

    def add(self, index: model.Index):
        self._add(index)
    
    def get_index_by_name(self, index_name) -> model.Index:
        return self._get_index_by_name(index_name)
    
    def add_docs_bulk(self, index_name, docs_bulk):
        self._add_docs(index_name, docs_bulk)

    @abc.abstractmethod
    def _add(self, index: model.Index):
        raise NotImplementedError

    @abc.abstractmethod
    def _add_docs_bulk(self, index_name, docs_bulk):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_index_by_name(self, index_name) -> model.Index:
        raise NotImplementedError
    


class ElasticIndexRepository(ElasticIndexRepositoryAbstract):
    def __init__(self, elasticsearch: AsyncElasticsearch) -> None:
        # super().__init__()
        self.elasticsearch = elasticsearch

    async def _add(self, index: model.Index):
        await self.elasticsearch.indices.create(index=index.index_name, mappings=index.mappings)
    
    async def _get_index_by_name(self, index_name) -> model.Index:
        return await self.elasticsearch.indices.get(index=index_name)
    
    async def _add_docs_bulk(self, index_name, docs_bulk):
        try:
            return await async_bulk(self.elasticsearch, docs_bulk)
        except:
            return False

