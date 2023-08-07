from pyharmonics.marketdata import BinanceCandleData, YahooOptionsData
from pyharmonics.search import HarmonicSearch
from pyharmonics import OHLCTechnicals, Position
from pyharmonics.plotter.harmonic import HarmonicPlotter, HarmonicPositionPlotter
from pyharmonics.plotter.option import OptionPlotter
import pandas as pd
import datetime

present = int(datetime.datetime.now().timestamp() * 1000)

b = BinanceCandleData()
b._set_params('BTCUSDT', b.HOUR_1, 1000)
b.df = pd.read_pickle("tests/data/btc_test_data")
t = OHLCTechnicals(b.df, b.symbol, b.interval, peak_spacing=10)
m = HarmonicSearch(t, fib_tolerance=0.03)
m.search()

def test_technicals_plotter():
    p = HarmonicPlotter(t, 'BTCUSDT', b.HOUR_1)
    p.add_peaks()
    p.add_matrix_plots(m.get_patterns(family=m.XABCD))
    p.show()

def test_position_plotter():
    patterns = m.get_patterns(family=m.XABCD)
    pattern = patterns[m.XABCD][0]
    position = Position(pattern, pattern.y[-1], 1000)
    p = HarmonicPositionPlotter(t, position)
    p.show()

def test_option_plotter():
    yo = YahooOptionsData('PLTR')
    yo.analyse_options(trend='volume')
    p = OptionPlotter(yo, yo.ticker.options[0])
    p.show()
