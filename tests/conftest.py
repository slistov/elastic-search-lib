from time import sleep
from typing import Dict

import pytest

from elastic_search_lib.service_layer.services import ElasticProvider


class FakeAsyncElasticSearch:
    class Indices:
        # ключ словаря - название индекса, значение - словарь из id документа и содержания документа
        __indices: Dict[str, Dict[int, str]] = {}        

        async def get(self, index):
            try:
                sleep(0.1)
                return self.__indices.get(index, None)
            except Exception as e:
                return None
        
        async def update(self, index, id, document):
            index_obj = await self.get(index)
            if not index_obj or not index_obj.get(id, None):
                self.__indices.update(
                    {
                        index: {
                            id: document
                        }
                    }
                )
            

    indices: Indices

    def __init__(self) -> None:
        self.indices = self.Indices()

    @pytest.mark.asyncio
    async def index(self, index, id, document):
        await self.indices.update(index, id, document)
    
    async def search(self, index, query):
        # Проверить все документы в индексе
        doc_dict = await self.indices.get(index)
        text = query['multi_match']['query']
        fields = query['multi_match']['fields']
        for doc_id, doc_body in doc_dict.items():
            for field_name, field_value in doc_body.items():
                if not field_name in fields: continue
                list_of_words = field_value.split()
                for word in list_of_words:
                    if word.startswith(text):
                        return {doc_id: doc_body}
        return False


#@pytest.fixture(scope='session')
async def es():
    es = FakeAsyncElasticSearch()
    await es.index('test_index', 1, {
        'doc_field1': 'some text to search: value', 
        'doc_field2': 'another one...'
    })
    return es


#@pytest.fixture
async def ep():
    es_async = await es()
    return ElasticProvider(es_async)
