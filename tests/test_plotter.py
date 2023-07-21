from pyharmonics.marketdata import BinanceCandleData
from pyharmonics.search import MatrixSearch
from pyharmonics import Technicals, Position
from pyharmonics.plotter import Plotter, PositionPlotter
import pandas as pd


b = BinanceCandleData()
b._set_params('BTCUSDT', b.HOUR_1, 1000)
b.df = pd.read_pickle("tests/data/btc_test_data")
t = Technicals(b.df, b.symbol, b.interval, peak_spacing=10)
m = MatrixSearch(t, fib_tolerance=0.03)
m.search()

def test_technicals_plotter():
    p = Plotter(t, 'BTCUSDT', b.HOUR_1)
    p.add_peaks()
    p.add_matrix_plots(m.get_patterns(family=m.XABCD))
    p.show()

def test_position_plotter():
    patterns = m.get_patterns(family=m.XABCD)
    pattern = patterns[m.XABCD][0]
    position = Position(pattern, pattern.y[-1], 1000)
    p = PositionPlotter(t, position)
    p.show()
