from elastic.domain import model
from typing import Dict, Any
from elastic.service_layer.services import ElasticProvider

class FakeElasticSearch:
    # ключ словаря - название индекса, значение - словарь из id документа и содержания документа
    indices: Dict[str, Dict[int, str]] = {}
    def index(self, index, id, document):
        if not self.indices.get('index', None) or not self.indices[index].get(id, None):
            self.indices.update(
                {
                    index: {
                        id: document
                    }
                }
            )
        
    def get(self, index, id):
        return self.indices.get(index, None).get(id, None)
    
    def search(self, index, text_to_search):
        # Проверить все документы в индексе
        for doc_id, doc_body in self.indices[index].items():
            list_of_words = doc_body.split()
            for word in list_of_words:
                if word.startswith(text_to_search):
                    return {doc_id: doc_body}
        return False

def test_quote_indexed_by_es_and_could_be_retrieved_by_id():
    qoute = model.Quote("Movie", "Bruce Lee", "Hey", "Эй", ['приветствие', 'оклик'])
    es = FakeElasticSearch()

    es.index('test_index', 1, {'doc': 'val'})
    assert es.get('test_index', 1) == {'doc': 'val'}


class TestElasticProvider:
    def test_creation(self):
        es = FakeElasticSearch()
        es.index('test_index', 1, {'doc': 'some text to search: value'})

        ep = ElasticProvider(es)
        assert ep.search(index='test_index', text_to_search='va')


