from pyharmonics.marketdata import BinanceCandleData, YahooOptionData
from pyharmonics.search import HarmonicSearch
from pyharmonics import OHLCTechnicals, Position, Technicals
from pyharmonics.plotter import HarmonicPlotter, PositionPlotter, Plotter, OptionPlotter
import pandas as pd
import datetime

present = int(datetime.datetime.now().timestamp() * 1000)

b = BinanceCandleData()
b._set_params('BTCUSDT', b.HOUR_1, 1000)
b.df = pd.read_pickle("tests/data/btc_test_data")
t = OHLCTechnicals(b.df, b.symbol, b.interval, peak_spacing=10)
m = HarmonicSearch(t, fib_tolerance=0.03)
m.search()

def test_ohlc_technicals_plotter():
    p = HarmonicPlotter(t)
    p.add_peaks()
    p.add_harmonic_plots(m.get_patterns(family=m.XABCD))
    p.show()

def test_single_technicals_plotter():
    of = pd.DataFrame(b.df[['close']])
    st = Technicals(of, 'BTSUSDT', b.HOUR_1)
    sm = HarmonicSearch(st, fib_tolerance=0.06)
    sm.search()
    p = Plotter(st)
    p.add_peaks()
    p.add_harmonic_plots(sm.get_patterns(family=sm.XABCD))
    p.show()

def test_position_plotter():
    patterns = m.get_patterns(family=m.XABCD)
    pattern = patterns[m.XABCD][0]
    position = Position(pattern, pattern.y[-1], 1000)
    p = PositionPlotter(t, position)
    p.show()

def test_option_plotter():
    yo = YahooOptionData('TSLA')
    yo.analyse_options(trend='volume')
    p = OptionPlotter(yo, yo.ticker.options[0])
    p.show()
