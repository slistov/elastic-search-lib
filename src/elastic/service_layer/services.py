from typing import Dict, List
from fastapi import HTTPException
from ..domain import model
from elasticsearch import AsyncElasticsearch, NotFoundError
from ..adapters.repository import ElasticIndexRepository, ElasticIndexRepositoryAbstract


class ElasticProvider:
    def __init__(self, es: AsyncElasticsearch) -> None:
        self.__es = es

    async def search(self, text, index = 'index-quote'):
        query = {
            "multi_match": {
                "query": text,
                "fields": ["quote", "movie", "speaker"],
                "type" : "phrase_prefix"                
            }            
        }
        response = await self.__es.search(index=index, query=query)
        return response


async def add_doc_to_index(elastic_repo: ElasticIndexRepositoryAbstract, index_name, docs_bulk):
    try:
        index = await elastic_repo.get_index_by_name(index_name)
    except NotFoundError:
        index = model.IndexQuote(index_name, docs_bulk)
        await elastic_repo.add(index)
    return await elastic_repo.add_docs_bulk(index_name=index_name, docs_bulk=docs_bulk)


async def search_index_for_text(elastic_repo: ElasticIndexRepositoryAbstract, index_name, text):
    return await elastic_repo.search(index_name=index_name, text=text)