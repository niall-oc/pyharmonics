from pyharmonics.marketdata import BinanceCandleData
import pandas as pd
import datetime

b = BinanceCandleData()

def test_BinanceCandleData():
    """
    Create a binance object and assert it converts dates to binance epoch
    """
    b._set_params('BTCUSDT', b.HOUR_1, num_candles=1000)
    b.df = pd.read_pickle("tests/data/btc_test_data")
    assert (len(b.df) == 1000)  # type:ignore
    assert (len(b.df.columns) == len(b.COLUMNS))  # type:ignore
    t = datetime.datetime(2020, 1, 1, 1, 1, 1)
    assert (b._datetime_to_epoch(t) == 1577840461000)

def test_get_candles():
    """
    Disabled because it requires hitting binance.  Prefix function with test_ to reactivate
    """
    b.get_candles('BTCUSDT', b.HOUR_1, num_candles=1000)
    assert (len(b.df) == 1000)
    b.get_candles('BTCUSDT', b.HOUR_1, num_candles=2000)
    assert (len(b.df) == 1999)
    assert (b.df.iloc[0][b.CLOSE_TIME] < b.df.iloc[-1][b.CLOSE_TIME])

def test_get_candles_start():
    """
    Disabled because it requires hitting binance.  Prefix function with test_ to reactivate
    """
    b.get_candles('BTCUSDT', b.HOUR_1, start=datetime.datetime(2022, 2, 10))
    assert (len(b.df) == 1000)

    # BINANCE BUG, when given starttime, num candles is ignored
    b.get_candles('BTCUSDT', b.HOUR_1, num_candles=2000, start=datetime.datetime(2022, 2, 10))
    assert (len(b.df) == 1999)
    assert (b.df.iloc[0][b.CLOSE_TIME] < b.df.iloc[-1][b.CLOSE_TIME])

def test_get_candles_end():
    """
    Disabled because it requires hitting binance.  Prefix function with test_ to reactivate
    """
    b.get_candles('BTCUSDT', b.HOUR_1, end=datetime.datetime(2023, 2, 10))
    assert (len(b.df) == 1000)

    b.get_candles('BTCUSDT', b.HOUR_1, num_candles=2000, end=datetime.datetime(2023, 2, 10))
    assert (len(b.df) == 1999)
    assert (b.df.iloc[0][b.CLOSE_TIME] < b.df.iloc[-1][b.CLOSE_TIME])

def test_get_candles_start_end():
    b.get_candles('BTCUSDT', b.HOUR_1, start=datetime.datetime(2022, 12, 10), end=datetime.datetime(2023, 2, 10))
    assert (len(b.df) == 1498)
    assert (b.df.iloc[0][b.CLOSE_TIME] < b.df.iloc[-1][b.CLOSE_TIME])
