import pytest
from conftest import ep

from elastic_search_lib import 


class TestElasticProvider:
    @pytest.mark.asyncio
    async def test_get(self):
        ep_async = await ep()
        assert await ep_async.get_index_by_name(index='test_index')
        assert not await ep_async.get_index_by_name(index='wrong_test_index')        
    
    @pytest.mark.asyncio
    async def test_search(self):
        ep_async = await ep()
        assert await ep_async.search(index='test_index', text='va', fields=["doc_field1", "doc_field2"])


