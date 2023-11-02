from pyharmonics.marketdata import BinanceCandleData, YahooOptionData
from pyharmonics.search import HarmonicSearch, DivergenceSearch
from pyharmonics import OHLCTechnicals, Position, Technicals
from pyharmonics.plotter import HarmonicPlotter, PositionPlotter, Plotter, OptionPlotter
import pandas as pd
import datetime

present = int(datetime.datetime.now().timestamp() * 1000)

b = BinanceCandleData()
b._set_params('BTCUSDT', b.HOUR_1, 1000)
b.df = pd.read_pickle("tests/data/btc_test_data")
t = OHLCTechnicals(b.df, b.symbol, b.interval, peak_spacing=10)
m = HarmonicSearch(t, fib_tolerance=0.03, strict=False)
m.search()

def test_XABCD():
    p = HarmonicPlotter(t)
    d = DivergenceSearch(t)
    d.search()
    p.add_peaks()
    p.add_harmonic_plots(m.get_patterns(family=m.XABCD))
    p.add_divergence_plots(d.get_patterns())
    p.show()

def test_XABCD_strict():
    m = HarmonicSearch(t, fib_tolerance=0.03, strict=True)
    m.search()
    p = HarmonicPlotter(t)
    d = DivergenceSearch(t)
    d.search()
    p.add_peaks()
    p.add_harmonic_plots(m.get_patterns(family=m.XABCD))
    p.add_divergence_plots(d.get_patterns())
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
    d = DivergenceSearch(t)
    d.search()
    p.add_divergence_plots(d.get_patterns())
    p.show()

def test_option_plotter():
    yo = YahooOptionData('WBA')
    yo.analyse_options(trend='openInterest')
    p = OptionPlotter(yo, yo.ticker.options[0])
    p.show()
