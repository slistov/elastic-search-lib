from scope.domain import model
from typing import Dict, Any

class FakeElasticSearch:
    indexes: Dict[str, Dict[int, Any]] = {}
    def index(self, index, id, document):
        if not self.indexes.get('index', None) or not self.indexes[index].get(id, None):
            self.indexes.update(
                {
                    index: {
                        id: document
                    }
                }
            )
        
    def get(self, index, id):
        return self.indexes.get(index, None).get(id, None)


# def test_get_token_from_header_returns_token():
def test_quote_indexed_by_es_and_could_be_retrieved_by_id():
    qoute = model.Quote("Movie", "Bruce Lee", "Hey", "Эй", ['приветствие', 'оклик'])
    es = FakeElasticSearch()

    es.index('test_index', 1, {'doc': 'val'})
    assert es.get('test_index', 1) == {'doc': 'val'}