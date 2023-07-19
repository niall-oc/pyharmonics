from pyharmonics.marketdata import BinanceCandleData, YahooCandleData
from pyharmonics.search import MatrixSearch
from pyharmonics import Technicals
from pyharmonics.plotter import Plotter
import pandas as pd
import datetime

present = int(datetime.datetime.now().timestamp() * 1000)

b = BinanceCandleData()
b._set_params('BTCUSDT', b.HOUR_1, 1000)
b.df = pd.read_pickle("tests/data/btc_test_data")
t = Technicals(b.df, peak_spacing=10)
m = MatrixSearch(t, fib_tolerance=0.03)
m.search()

def test_technicals_plotter():
    p = Plotter(t, 'BTCUSDT', b.HOUR_1)
    p.add_peaks()
    p.add_matrix_plots(m.get_patterns(family=m.XABCD))
    p.main_plot.show()
