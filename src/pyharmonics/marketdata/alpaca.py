
from pyharmonics.marketdata.candle_base import CandleData
import pandas as pd
from numpy import int64
from alpaca_trade_api import REST, TimeFrame, TimeFrameUnit
import datetime


class AlpacaCandleData(CandleData):
    """
    If you want to get market data or prices for crypto currencies, you can use this class.
    This class is a subclass of CandleData and is used to get candle data from Alpaca.

    >>> m = BinanceCandleData() # 200 1 hour candles of BTCUSDT price history

    >>> m.get_candles('BTCUSDT', '1h', num_candles=1000) # 1000 1 hour candles of BTCUSDT price history

    >>> m.get_candles('BTCUSDT', '1h', num_candles=1000, end=datetime.datetime(2020, 3, 21, 14, 0, 15))
    # 1000 1 hour candles of BTCUSDT price history leading up to 21st march 2020

    >>> m.get_candles('BTCUSDT', '1h', num_candles=1000, start=datetime.datetime(2020, 3, 21, 14, 0, 15))
    # 1000 candle data from 21st of march 2020 until present

    >>> m.get_candles('BTCUSDT', '1h', start=datetime.datetime(2020, 3, 21, 14, 0, 15))
    # All candle data from 21st of march 2020 until present
    """
    # Critical Binance will not return more than 1000 candles of data per call.
    MAX_CANDLES = 1000
    SOURCE = 'Alpaca'
    INTERVALS = {
        CandleData.MIN_1: TimeFrame(1, TimeFrameUnit.Minute),
        CandleData.MIN_3: TimeFrame(3, TimeFrameUnit.Minute),
        CandleData.MIN_5: TimeFrame(5, TimeFrameUnit.Minute),
        CandleData.MIN_15: TimeFrame(15, TimeFrameUnit.Minute),
        CandleData.MIN_30: TimeFrame(30, TimeFrameUnit.Minute),
        CandleData.MIN_45: TimeFrame(45, TimeFrameUnit.Minute),
        CandleData.HOUR_1: TimeFrame(1, TimeFrameUnit.Hour),
        CandleData.HOUR_2: TimeFrame(2, TimeFrameUnit.Hour),
        CandleData.HOUR_4: TimeFrame(4, TimeFrameUnit.Hour),
        CandleData.HOUR_8: TimeFrame(8, TimeFrameUnit.Hour),
        CandleData.DAY_1: TimeFrame(1, TimeFrameUnit.Day),
        CandleData.WEEK_1: TimeFrame(1, TimeFrameUnit.Week),
        CandleData.MONTH_1: TimeFrame(1, TimeFrameUnit.Month)
    }
    TIME_DELTA = {
        CandleData.MIN_1: datetime.timedelta(minutes=1),
        CandleData.MIN_3: datetime.timedelta(minutes=3),
        CandleData.MIN_5: datetime.timedelta(minutes=4),
        CandleData.MIN_15: datetime.timedelta(minutes=15),
        CandleData.MIN_30: datetime.timedelta(minutes=30),
        CandleData.MIN_45: datetime.timedelta(minutes=45),
        CandleData.HOUR_1: datetime.timedelta(hours=1),
        CandleData.HOUR_2: datetime.timedelta(hours=2),
        CandleData.HOUR_4: datetime.timedelta(hours=4),
        CandleData.HOUR_8: datetime.timedelta(hours=8),
        CandleData.DAY_1: datetime.timedelta(days=1),
        CandleData.WEEK_1: datetime.timedelta(weeks=1),
        CandleData.MONTH_1: datetime.timedelta(days=30)
    }

    def __init__(self, key, schema=None, time_zone='Europe/Dublin', df_index=CandleData.DTS):
        """
        Constructor for AlpacaCandleData

        >>> a = AlpacaCandleData()
        >>> a = AlpacaCandleData(schema=[{"name": "open_time", "type": "int64"}, {"name": "open", "type": "float"}])
        >>> a = AlpacaCandleData(time_zone='Europe/Dublin')

        :param list schema: The schema for the candle data.  If None, the default schema is used.
        :param str time_zone: The time zone to use for the data.
        :param str df_index: The index to use for the dataframe.  If None, the default index is used.
        """
        # Binance returns a list of lists. There is no schema as such and typing must be defined in line with biances API.
        # Making the schema a paramater means it can be updated using a config and no code change.
        # Data types are pandas series data types.
        if schema is None:
            self.schema = [
                {"name": self.OPEN, "type": "float"},
                {"name": self.HIGH, "type": "float"},
                {"name": self.LOW, "type": "float"},
                {"name": self.CLOSE, "type": "float"},
                {"name": self.VOLUME, "type": "float"},
                {"name": "trade_count", "type": "int"},
                {"name": "vwap", "type": "float"}
            ]

        self.columns = [c['name'] for c in self.schema]
        # Binance can be queried for read only operations without an API key.
        self.rc = REST(key['api'], key['secret'])
        # time zone reflects must be set to correct region otherwise patern detection may produce strange time points.
        self.time_zone = time_zone
        self.df = None
        self.candle_gap = None
        if df_index in (self.DTS, self.CLOSE_TIME):
            self.df_index = df_index
        else:
            raise ValueError(f'df_index must be one of "{self.DTS}" or "{self.CLOSE_TIME}"')

    def _datetime_to_epoch(self, t):
        """
        Overridden method to convert datetime to epoch

        >>> a._datetime_to_epoch(datetime.datetime(2020, 3, 21, 14, 0, 15))
        1584792015

        :param t: datetime.datetime
        :return: int
        """
        if t is None:
            return None
        elif isinstance(t, (int, float, int64)):
            # If an epoch is given with decimals simply cast of the decimals
            return datetime.date.fromtimestamp(int(t))
        elif isinstance(t, (datetime.datetime,)):
            # Date time must be converted to epoch
            return t.timestamp()
        else:
            raise ValueError('alpaca date must be datetime or timestamp')

    def _to_dataframe(self, data):
        """
        Converts the raw data from the API into a pandas dataframe.

        >>> a._to_dataframe(data)

        :param data: The raw data from the API.
        :return: The pandas dataframe
        """
        df = pd.DataFrame(data=data, columns=self.columns)

        for col in self.schema:
            df[col['name']] = df[col['name']].astype(col['type'])

        df[self.DTS] = pd.to_datetime(df[self.CLOSE_TIME], unit='ms', utc=True).dt.tz_convert(self.time_zone)
        df = df[self.COLUMNS]  # Hold on to only the essentials and save memory
        return df

    def get_candles(self, symbol: str, interval: TimeFrame, num_candles=None, start=None, end=None):
        """
        If start and end are defined all candles between those time ranges will be pulled
        and stored in self.df.  This is done using multiple calls.
        This is done in blocks of 1000 candles.

        If only start or end or both are None, then a single call is made.
        If num_candles is greater than 1000 then multiple calls are made to get the data.

        >>> a.get_candles('BTCUSDT', TimeFrame(1, TimeFrameUnit.Hour), num_candles=1000)
        >>> a.get_candles('BTCUSDT', TimeFrame(1, TimeFrameUnit.Hour), start=datetime.datetime(2020, 3, 21, 14, 0, 15))
        >>> a.get_candles('BTCUSDT', TimeFrame(1, TimeFrameUnit.Hour), end=datetime.datetime(2020, 3, 21, 14, 0, 15))

        :param symbol: The symbol to fetch.
        :param interval: The interval to fetch.
        :param num_candles: The number of candles to fetch.
        :param start: The start time for a range of candles.
        :param end: The end time for a range of candles.
        """
        # If no end time then now - 1000 time frames
        self._set_params(symbol, interval, num_candles, start, end)
        if self.num_candles:
            self.start = datetime.datetime.now() - (self.TIME_DELTA[self.interval] * self.num_candles * 2)
            self.df = self.rc.get_bars(self.symbol, self.INTERVALS[self.interval], self.start.date()).df
            self.df[self.CLOSE_TIME] = self.df.index.map(lambda d: self._datetime_to_epoch(d))
            self.df[self.DTS] = pd.to_datetime(self.df[self.CLOSE_TIME], unit='s', utc=True).dt.tz_convert(self.time_zone)
            self.reset_index()
        elif self.start and self.end:
            if self.end and self.end.date() == datetime.date.today():
                self.df = self.rc.get_bars(self.symbol, self.INTERVALS[self.interval], self.start.date()).df
            else:
                self.df = self.rc.get_bars(self.symbol, self.INTERVALS[self.interval], self.start.date(), self.end.date()).df
            self.df[self.CLOSE_TIME] = self.df.index.map(lambda d: self._datetime_to_epoch(d))
            self.df[self.DTS] = pd.to_datetime(self.df[self.CLOSE_TIME], unit='s', utc=True).dt.tz_convert(self.time_zone)
            self.reset_index()
