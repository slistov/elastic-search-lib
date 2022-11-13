from pytest import fixture
from typing import Dict
from elastic_search_lib.service_layer.services import ElasticProvider


class FakeAsyncElasticSearch:
    class Indices:
        # ключ словаря - название индекса, значение - словарь из id документа и содержания документа
        __indices: Dict[str, Dict[int, str]] = {}        
        def get(self, index):
            async def get(self, index):
                if index:
                    return self.__indices.get(index, None)
                else:
                    return None

    indices: Indices
    def __init__(self) -> None:
        self.indices = self.Indices()

    def index(self, index, id, document):
        if not self.indices.get('index') or not self.indices.get(index).get(id, None):
            self.indices.update(
                {
                    index: {
                        id: document
                    }
                }
            )

    def search(self, index, text):
        # Проверить все документы в индексе
        for doc_id, doc_body in self.indices.get(index).items():
            list_of_words = doc_body.split()
            for word in list_of_words:
                if word.startswith(text):
                    return {doc_id: doc_body}
        return False


@fixture(scope='session')
def es():
    es = FakeAsyncElasticSearch()
    es.index('test_index', 1, {'doc': 'some text to search: value'})
    return es


@fixture
def ep(es):
    return ElasticProvider(es)
