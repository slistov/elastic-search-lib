from elasticsearch import AsyncElasticsearch
from fastapi import Body, Depends, FastAPI, Response, status
from fastapi.encoders import jsonable_encoder

import elastic.entrypoints.schemas as schemas

from .. import config
from ..service_layer import services
from . import dependencies 

app = FastAPI()


@app.put("/indices/{index}")
async def api_indexes_add(index: str, docs_bulk = Body()):
    elastic_repo = dependencies.elastic_repo
    return await services.add_doc_to_index(elastic_repo, index, docs_bulk)


@app.get("/indices/{index}")
async def api_search_index_for_text(index, text):
    es = dependencies.es
    ep = services.ElasticProvider(es=es)
    return await ep.search(text=text, index=index)


