import pytest
from elastic_search_lib.domain import model
from typing import Dict


class TestElasticProvider:
    @pytest.mark.asyncio
    async def test_get(self, ep):
        assert await ep.get_index_by_name(index='test_index')
    
    @pytest.mark.asyncio
    async def test_search(self, ep):
        assert await ep.search(index='test_index', text='va')


