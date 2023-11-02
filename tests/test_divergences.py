from pyharmonics import constants
from pyharmonics.marketdata import BinanceCandleData
from pyharmonics.search import DivergenceSearch
from pyharmonics.technicals import OHLCTechnicals
import pandas as pd

b = BinanceCandleData()
b._set_params('BTCUSDT', b.HOUR_1, 1000, None, None)
b.df = pd.read_pickle("tests/data/btc_test_data")
t = OHLCTechnicals(b.df, b.symbol, b.interval, peak_spacing=10)

def test_divergence_search():
    d = DivergenceSearch(t)
    d.search(limit_to=100)
    found = d.get_patterns()
    print(len(found[t.RSI]))
    print(len(found[t.MACD]))
    assert len(found[t.RSI]) == 48
    assert len(found[t.MACD]) == 48
