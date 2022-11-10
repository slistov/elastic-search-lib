from typing import List

from fastapi import Depends, Header, HTTPException

from ..service_layer import services
from ..adapters.repository import ElasticIndexRepository
from .. import config
from elasticsearch import AsyncElasticsearch

user, password = config.get_es_user_credentials()
es = AsyncElasticsearch(
    config.get_es_uri(), 
    basic_auth=(user, password),
    verify_certs=False
)

elastic_repo = ElasticIndexRepository(es)
