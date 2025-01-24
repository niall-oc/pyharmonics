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
h = HarmonicSearch(t, fib_tolerance=0.03)
h.search()
h.forming()

def test_XABCD():
    p = HarmonicPlotter(t)
    d = DivergenceSearch(t)
    d.search()
    p.add_peaks()
    p.add_harmonic_plots(h.get_patterns(family=h.XABCD))
    p.add_divergence_plots(d.get_patterns())
    p.show()

def test_ABCD():
    m = HarmonicSearch(t, fib_tolerance=0.03, check_false_anchor=False)
    m.search()
    p = HarmonicPlotter(t)
    d = DivergenceSearch(t)
    d.search()
    p.add_peaks()
    p.add_harmonic_plots(m.get_patterns(family=m.ABCD))
    p.add_divergence_plots(d.get_patterns())
    p.show()

def test_ABCD_anchor():
    m = HarmonicSearch(t, fib_tolerance=0.03, check_false_anchor=True)
    m.search()
    p = HarmonicPlotter(t)
    d = DivergenceSearch(t)
    p.title = p.plot_title + 'ANCHOR FLAG'
    d.search()
    p.add_peaks()
    p.add_harmonic_plots(m.get_patterns(family=m.ABCD))
    p.add_divergence_plots(d.get_patterns())
    p.show()

def test_single_technicals_plotter():
    of = pd.DataFrame(b.df[['close']])
    st = Technicals(of, 'BTSUSDT', b.HOUR_1)
    sh = HarmonicSearch(st, fib_tolerance=0.06)
    sh.search()
    p = Plotter(st)
    p.add_peaks()
    p.add_harmonic_plots(sh.get_patterns(family=sh.XABCD))
    p.show()

def test_position_plotter_formed():
    patterns = h.get_patterns(family=h.XABCD)
    pattern = patterns[h.XABCD][0]
    position = Position(pattern, pattern.y[-1], 1000)
    p = PositionPlotter(t, position)
    d = DivergenceSearch(t)
    d.search()
    p.add_divergence_plots(d.get_patterns())
    p.show()

def test_position_plotter_forming():
    patterns = h.get_patterns(family=h.ABCD, formed=False)
    pattern = patterns[h.ABCD][0]
    position = Position(pattern, pattern.y[-1], 1000)
    p = PositionPlotter(t, position)
    d = DivergenceSearch(t)
    d.search()
    p.add_divergence_plots(d.get_patterns())
    p.show()

def test_option_plotter():
    yo = YahooOptionData('AAPL')
    yo.analyse_options(trend='volume')
    p = OptionPlotter(yo, yo.ticker.options[0])
    p.show()
