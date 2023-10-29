from pyharmonics.marketdata import YahooCandleData, BinanceCandleData, YahooOptionData
from pyharmonics.technicals import OHLCTechnicals, Technicals
from pyharmonics.search import HarmonicSearch
from pyharmonics.positions import Position
from pyharmonics.plotter import HarmonicPlotter, PositionPlotter, OptionPlotter


def play_position(hs, pattern, strike, dollar_amount):
    pos = Position(pattern, strike, dollar_amount)
    p = PositionPlotter(hs.td, pos)
    p.add_peaks()
    p.show()

def whats_new(cd, limit_to=-1):
    t = OHLCTechnicals(cd.df, cd.symbol, cd.interval)
    hs = HarmonicSearch(t)
    hs.search(limit_to=limit_to)
    p = HarmonicPlotter(t)
    p.add_peaks()
    p.add_harmonic_plots(hs.get_patterns(hs.XABCD))
    p.add_harmonic_plots(hs.get_patterns(hs.ABCD))
    p.add_harmonic_plots(hs.get_patterns(hs.ABC))
    p.show()
    return hs

def whats_new_binance(symbol, interval, limit_to=-1):
    bc = BinanceCandleData()
    bc.get_candles(symbol, interval, 1000)
    whats_new(bc, limit_to=limit_to)

def whats_new_yahoo(symbol, interval, limit_to=-1):
    yc = YahooCandleData()
    yc.get_candles(symbol, interval)
    whats_new(yc, limit_to=limit_to)

def whats_options_volume(symbol):
    yo = YahooOptionData(symbol)
    yo.analyse_options(trend='volume')
    p = OptionPlotter(yo, yo.ticker.options[0])
    p.show()

def whats_options_interest(symbol):
    yo = YahooOptionData(symbol)
    yo.analyse_options()
    p = OptionPlotter(yo, yo.ticker.options[0])
    p.show()
