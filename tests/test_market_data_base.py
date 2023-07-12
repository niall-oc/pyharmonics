from pyharmonics.market_data.base import MarketData
import pytest

def test_example():
    with pytest.raises(TypeError):
        m = MarketData()
