from pyharmonics.marketdata import YahooCandleData, BinanceCandleData, YahooOptionData
from pyharmonics.technicals import OHLCTechnicals, Technicals
from pyharmonics.search import HarmonicSearch, DivergenceSearch
from pyharmonics.positions import Position
from pyharmonics.plotter import HarmonicPlotter, PositionPlotter, OptionPlotter
from pyharmonics import constants


def play_position(hs, pattern, strike, dollar_amount):
    pos = Position(pattern, strike, dollar_amount)
    p = PositionPlotter(hs.td, pos)
    p.add_peaks()
    p.show()

def whats_new(cd, limit_to=-1):
    """
    Search for new harmonic patterns and divergences in the given data.

    :param cd: The CandleData object to search.
    :param limit_to: Limit the results to patterns that complete in that last n candles.
    :return: The HarmonicSearch object containing the results.
    """
    t = OHLCTechnicals(cd.df, cd.symbol, cd.interval)
    hs = HarmonicSearch(t)
    hs.search(limit_to=limit_to)
    p = HarmonicPlotter(t)
    d = DivergenceSearch(t)
    d.search()
    p.add_peaks()
    p.add_harmonic_plots(hs.get_patterns(family=hs.XABCD))
    p.add_harmonic_plots(hs.get_patterns(family=hs.ABCD))
    p.add_harmonic_plots(hs.get_patterns(family=hs.ABC))
    p.add_divergence_plots(d.get_patterns())
    p.show()
    return hs

def whats_new_binance(symbol, interval, limit_to=-1, candles=1000):
    """
    Search for new harmonic patterns and divergences in the given Binance data.

    >>> harmonic_search = whats_new_binance('BTCUSDT', BinanceCandleData.HOUR_1, limit_to=10, candles=1000)
    >>> harmonic_search.get_patterns()

    >>> harmonic_search = whats_new_binance('BTCUSDT', '1d', candles=1000)
    >>> harmonic_search.get_patterns()

    :param symbol: The symbol to search.
    :param limit_to: Limit the results to patterns that complete in that last n candles.
    :param candles: The number of candles to fetch.
    :return: The HarmonicSearch object containing the results.
    """
    bc = BinanceCandleData()
    bc.get_candles(symbol, interval, candles)
    return whats_new(bc, limit_to=limit_to)

def whats_new_yahoo(symbol, interval, limit_to=-1, candles=1000):
    """
    Search for new harmonic patterns and divergences in the given Yahoo data.

    >>> harmonic_search = whats_new_yahoo('AAPL', YahooCandleData.DAY_1, limit_to=10, candles=1000)
    >>> harmonic_search.get_patterns()

    >>> harmonic_search = whats_new_yahoo('AAPL', '1d', candles=1000)
    >>> harmonic_search.get_patterns()

    :param symbol: The symbol to search.
    :param interval: The timeframe or interval to search on.
    :param limit_to: Limit the results to patterns that complete in that last n candles.
    :param candles: The number of candles to fetch.
    :return: The HarmonicSearch object containing the results.
    """
    yc = YahooCandleData()
    yc.get_candles(symbol, interval, candles)
    return whats_new(yc, limit_to=limit_to)

def whats_forming(cd, limit_to=10, percent_complete=0.8):
    """
    Search for forming harmonic patterns and divergences in the given data.

    :param cd: The CandleData object to search.
    :param limit_to: Limit the results to patterns that complete in that last n candles.
    :param percent_complete: The percentage of the pattern that must be complete.
    :return: The HarmonicSearch object containing the results.
    """
    t = OHLCTechnicals(cd.df, cd.symbol, cd.interval)
    hs = HarmonicSearch(t)
    hs.forming(limit_to=limit_to, percent_c_to_d=percent_complete)
    p = HarmonicPlotter(t)
    d = DivergenceSearch(t)
    d.search()
    p.add_peaks()
    p.add_harmonic_plots(hs.get_patterns(family=hs.XABCD, formed=False))
    p.add_harmonic_plots(hs.get_patterns(family=hs.ABCD, formed=False))
    p.add_harmonic_plots(hs.get_patterns(family=hs.ABC, formed=False))
    p.add_divergence_plots(d.get_patterns())
    p.show()
    return hs

def whats_forming_binance(symbol, interval, limit_to=10, percent_complete=0.8, candles=1000):
    """
    Search for forming harmonic patterns and divergences in the given Binance data.

    >>> harmonic_search = whats_forming_binance('BTCUSDT', BinanceCandleData.HOUR_1, limit_to=10, percent_complete=0.8, candles=1000)
    >>> harmonic_search.get_patterns()

    >>> harmonic_search = whats_forming_binance('BTCUSDT', '1d', candles=1000)
    >>> harmonic_search.get_patterns()

    :param symbol: The symbol to search.
    :param interval: The timeframe or interval to search on.
    :param limit_to: Limit the results to patterns that complete in that last n candles.
    :param percent_complete: The percentage of the pattern that must be complete.
    :param candles: The number of candles to fetch.
    :return: The HarmonicSearch object containing the results.
    """
    bc = BinanceCandleData()
    bc.get_candles(symbol, interval, candles)
    return whats_forming(bc, limit_to=limit_to, percent_complete=percent_complete)

def whats_forming_yahoo(symbol, interval, limit_to=10, percent_complete=0.8, candles=1000):
    """
    Search for forming harmonic patterns and divergences in the given Yahoo data.

    >>> harmonic_search = whats_forming_yahoo('AAPL', YahooCandleData.DAY_1, limit_to=10, percent_complete=0.8, candles=1000)
    >>> harmonic_search.get_patterns()

    >>> harmonic_search = whats_forming_yahoo('AAPL', '1d', candles=1000)
    >>> harmonic_search.get_patterns()

    :param symbol: The symbol to search.
    :param interval: The timeframe or interval to search on.
    :param limit_to: Limit the results to patterns that complete in that last n candles.
    :param percent_complete: The percentage of the pattern that must be complete.
    :param candles: The number of candles to fetch.
    :return: The HarmonicSearch object containing the results.
    """
    yc = YahooCandleData()
    yc.get_candles(symbol, interval, candles)
    return whats_forming(yc, limit_to=limit_to, percent_complete=percent_complete)

def whats_options_volume(symbol):
    """
    Displays the options volume for the given symbol.
    The volume is the number of contracts traded for the day.
    A plot illustrates the point of minimum losses for the market maker.

    :param symbol: The symbol to search.
    :return: The YahooOptionData object containing the results.
    """
    yo = YahooOptionData(symbol)
    yo.analyse_options(trend='volume')
    p = OptionPlotter(yo, yo.ticker.options[0])
    p.show()
    return yo

def whats_options_interest(symbol):
    """
    Displays the options open interest for the given symbol.
    The open interest is the number of contracts that are open.
    A plot illustrates the point of minimum losses for the market maker.

    :param symbol: The symbol to search.
    :return: The YahooOptionData object containing the results.
    """
    yo = YahooOptionData(symbol)
    yo.analyse_options()
    p = OptionPlotter(yo, yo.ticker.options[0])
    p.show()
    return yo
