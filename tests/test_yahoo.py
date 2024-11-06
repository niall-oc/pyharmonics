from pyharmonics.marketdata import YahooCandleData, YahooOptionData
import pandas as pd
import datetime

y = YahooCandleData()

def test_YahooCandleData_DAY_1():
    """
    Read a test block of 1000 MSFT 1day candles.
    Assetr the basic candle dataframe features work.
    """
    y._set_params('MSFT', y.DAY_1, num_candles=1000)
    y.df = pd.read_pickle('tests/data/msft_test_data')
    y.reset_index(index=y.DTS)

    assert (len(y.df) == 1000)  # type:ignore
    assert (len(y.df.columns) == len(y.COLUMNS))  # type:ignore
    t = datetime.datetime(2020, 1, 1, 1, 1, 1)
    assert (y._datetime_to_epoch(t) == 1577840461)

def test_YahooCandleData_WEEK_1():
    """
    Read a test block of 1000 MSFT 1day candles.
    Assetr the basic candle dataframe features work.
    """
    y.get_candles('WBA', y.WEEK_1, num_candles=1000)

    assert (len(y.df) == 1000)  # type:ignore
    assert (len(y.df.columns) == len(y.COLUMNS))  # type:ignore

def test_YahooOptionData():
    """
    Analyse options for stock
    """
    yo = YahooOptionData('TSLA')
    yo.analyse_options()
    assert isinstance(yo.ticker.options[0], str)

def test_get_candles():
    """
    """
    y.get_candles('MSFT', y.HOUR_1, num_candles=1000)
    assert (len(y.df) == 1000)
    y.get_candles('MSFT', y.HOUR_1, num_candles=2000)
    assert (len(y.df) > 1000)
    assert (y.df.iloc[0][y.CLOSE_TIME] < y.df.iloc[-1][y.CLOSE_TIME])

def test_get_candles_start():
    """
    """
    y.get_candles('MSFT', y.DAY_1, start=datetime.datetime(2024, 2, 10))
    assert (len(y.df) > 60)

    y.get_candles('MSFT', y.HOUR_1, num_candles=1000, start=datetime.datetime(2023, 2, 10))
    assert (len(y.df) == 1000)
    assert (y.df.iloc[0][y.CLOSE_TIME] < y.df.iloc[-1][y.CLOSE_TIME])

def test_get_candles_end():
    """
    end dates alone are not supported by Yahoo!
    """
    y.get_candles('MSFT', y.MIN_1, end=datetime.datetime.today())
    assert (len(y.df) > 0)


def test_get_candles_start_end():
    y.get_candles('MSFT', y.HOUR_1, start=datetime.datetime(2022, 12, 10), end=datetime.datetime(2023, 2, 10))
    assert (len(y.df) == 287)
    assert (y.df.iloc[0][y.CLOSE_TIME] < y.df.iloc[-1][y.CLOSE_TIME])
