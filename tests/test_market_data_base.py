from pyharmonics.marketdata.candle_base import CandleData
import pytest

def test_marketdata():
    with pytest.raises(TypeError):
        m = CandleData()
