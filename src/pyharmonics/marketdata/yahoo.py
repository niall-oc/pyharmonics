from pyharmonics.marketdata.candle_base import CandleData
import yfinance as yf
import pandas as pd
import math


class YahooCandleData(CandleData):
    """
    >>> m = YahooCandleData() # 200 1 hour candles of BTCUSDT price history

    >>> m.get_candles('MSFT', '1h', num_candles=1000) # 1000 1 hour candles of BTCUSDT price history

    >>> m.get_candles('MSFT', '1h', num_candles=1000, end=datetime.datetime(2020, 3, 21, 14, 0, 15))
    # 1000 1 hour candles of MSFT price history leading up to 21st march 2020

    >>> m.get_candles('MSFT', '1h', num_candles=1000, start=datetime.datetime(2020, 3, 21, 14, 0, 15))
    # 1000 candle data from 21st of march 2020 until present

    >>> m.get_candles('MSFT', '1h', start=datetime.datetime(2020, 3, 21, 14, 0, 15))
    # All candle data from 21st of march 2020 until present
    """
    MAX_CANDLES = 10000
    SOURCE = 'Yahoo'
    SHORT_INTERVALS = {'m': 1440, 'h': 24, 'd': 1}  # Bring hours or minutes to days
    LONG_INTERVALS = {'w': 4, 'M': 1}  # Bring Weeks or months to months
    INTERVALS = {
        CandleData.MIN_1: '1m',
        CandleData.MIN_5: '5m',
        CandleData.MIN_15: '15m',
        CandleData.HOUR_1: '60m',
        CandleData.DAY_1: '1d',
        CandleData.WEEK_1: '1wk',
        CandleData.MONTH_1: '1mo',
        CandleData.MONTH_3: '3mo'
    }
    LIMITS = {
        CandleData.MIN_1: '7d',
        CandleData.MIN_5: '60d',
        CandleData.MIN_15: '60d',
        CandleData.HOUR_1: '730d',
        CandleData.DAY_1: '10000mo',
        CandleData.WEEK_1: '10000mo',
        CandleData.MONTH_1: '10000mo',
        CandleData.MONTH_3: '10000mo'
    }

    def __init__(self, schema=None, time_zone='Europe/Dublin', df_index=CandleData.DTS):
        """
        >>> y = Yahoo()
        >>> y.get_candles('MSFT', '1d')

        Parameters
        ----------
        schema: list [dict...]
            A list of dictionaries containing column names and types.
        time_zone: str
            Used to localize time for candle data
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
                {"name": "dividends", "type": "float"},
                {"name": "stock_splits", "type": "int"}
            ]
        self.columns = [c['name'] for c in self.schema]
        self.time_zone = time_zone
        self.df = None
        self.candle_gap = None
        if df_index in (self.DTS, self.CLOSE_TIME):
            self.df_index = df_index
        else:
            raise ValueError(f'df_index must be one of "{self.DTS}" or "{self.CLOSE_TIME}"')

    def get_candles(self, symbol, interval, num_candles=None, start=None, end=None):
        """
        >>> y = Yahoo()
        >>> y.get_candles('MSFT', '1d')

        Parameters
        ----------
        asset_symbol : str
            The ticker identifier for the asset in question. eg.  'BTCUSDT' or 'META' or 'GOLD'
        interval: str
            eg. '1h' hour, '1m' minute, '1d' day. Use trigger.constants to avoid making mistakes here.
        num_candles: int
            The number of candles.  default is 200 candle intervals.
        start: datetime.datetime
            Specific start time for candle data.  This is internally converted into the time format required by Yahoo
        end: datetime.datetime
            Specific end time for candle data.  This is internally converted into the time format required by Yahoo
        """
        self.df = None
        self._set_params(symbol, interval, num_candles=num_candles, start=start, end=end)

        tick = yf.Ticker(self.symbol)
        self.df = tick.history(
            period=self.LIMITS[self.interval],
            interval=self.interval,
            start=self._epoch_to_datetime(self.start),
            end=self._epoch_to_datetime(self.end)
        )
        self._trim_data()

        rename_columns = {c: c.lower().replace(' ', '_') for c in self.df.columns}
        self.df = self.df.rename(columns=rename_columns)
        self.df[self.CLOSE_TIME] = self.df.index.map(lambda d: self._datetime_to_epoch(d))
        self.df[self.DTS] = pd.to_datetime(self.df[self.CLOSE_TIME], unit='s', utc=True).dt.tz_convert(self.time_zone)
        self.reset_index()

    def _trim_data(self):
        if self.start and self.end:
            pass
        elif self.start and not self.end:
            self.df = self.df[:min(len(self.df), self.num_candles)]
        else:
            self.df = self.df[max(len(self.df) - self.num_candles, 0):]

if __name__ == '__main__':
    y = YahooCandleData()
    y.get_candles('MSFT', y.HOUR_1, 200)
