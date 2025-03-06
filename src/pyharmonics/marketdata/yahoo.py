__author__ = 'github.com/niall-oc'

from pyharmonics.marketdata.candle_base import CandleData
import yfinance as yf
import pandas as pd

class YahooOptionChain:
    """
    YahooOptionChain is a class for analyzing options data from Yahoo Finance.

    >>> y = YahooOptionChain(option_chain)
    >>> y = YahooOptionChain(option_chain, top=30, trend='openInterest')
    """
    def __init__(self, option_chain, top=30, trend='openInterest'):
        """
        Constructor for YahooOptionChain

        >>> y = YahooOptionChain(option_chain)
        >>> y = YahooOptionChain(option_chain, top=30, trend='openInterest')

        :param yfinance.Ticker ticker: the yfinance Ticker object representing an asset.
        :params int top: the top 30 options, ranked by openInterest, are analyzed by default.
        """
        self.trend = trend
        self.calls = option_chain.calls
        self.calls = self.calls.sort_values(by=[trend], ascending=False)[:top]
        self.calls = self.calls.sort_values(by=['strike'])
        self.calls['oi_cumsum'] = self.calls[trend].cumsum()
        limit = min(self.calls['strike'])
        self.calls['losses'] = self.calls.apply(lambda row: (row['strike'] - limit) * row['oi_cumsum'] * 100, axis=1)

        self.puts = option_chain.puts
        self.puts = self.puts.sort_values(by=[trend], ascending=False)[:top]
        self.puts = self.puts.sort_values(by=['strike'])
        self.puts['oi_cumsum'] = self.puts.loc[::-1, trend].cumsum()[::-1]
        limit = max(self.puts['strike'])
        self.puts['losses'] = self.puts.apply(lambda row: (limit - row['strike']) * row['oi_cumsum'] * 100, axis=1)

        self.losses = self.calls[['strike', 'losses']].merge(self.puts[['strike', 'losses']], on='strike', how='outer').sort_values(by='strike')
        self.losses['losses_x'] = self.losses['losses_x'].ffill().fillna(0.0)
        self.losses['losses_y'] = self.losses['losses_y'].bfill().fillna(0.0)
        self.losses['pain'] = self.losses['losses_x'] + self.losses['losses_y']
        self.losses['pain'] = self.losses['pain'].map(lambda x: x or None).ffill().bfill()
        try:
            self.min_pain = list(self.losses.loc[self.losses['pain'] == min(self.losses['pain'])].to_dict()['strike'].values())[0]
        except TypeError:
            # Early in the trading day options data has None values
            self.min_pain = 0.0


class YahooOptionData:
    """
    YahooOptionData is a class for analyzing options data from Yahoo Finance.

    >>> y = YahooOptionData('AAPL')
    >>> y = YahooOptionData('AAPL').analyse_options(top=30, trend='volume')
    >>> y = YahooOptionData('AAPL').analyse_options(top=30, trend='openInterest')
    """
    def __init__(self, symbol):
        """
        Constructor for YahooOptionData

        >>> y = YahooOptionData('AAPL')
        """
        self.symbol = symbol
        self.ticker = yf.Ticker(self.symbol)
        self.options = {}
        self.price = float(self.ticker.fast_info['lastPrice'])

    def analyse_options(self, top=30, trend='openInterest'):
        """
        Analyze the options data for the given asset.

        >>> y = YahooOptionData('AAPL').analyse_options(top=30, trend='volume')
        >>> y = YahooOptionData('AAPL').analyse_options(top=30, trend='openInterest')

        :params int top: the top 30 options, ranked by openInterest, are analyzed by default.
        """
        for expiry in self.ticker.options:
            self.options[expiry] = YahooOptionChain(self.ticker.option_chain(expiry), top=top, trend=trend)

class YahooCandleData(CandleData):
    """
    YahooCandleData is a class for fetching candle data from Yahoo Finance.
    It is a subclass of CandleData and inherits all of its methods and attributes.

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
        CandleData.MIN_30: '15m',
        CandleData.HOUR_1: '60m',
        CandleData.DAY_1: '1d',
        CandleData.DAY_5: '5d',
        CandleData.WEEK_1: '1wk',
        CandleData.MONTH_1: '1mo',
        CandleData.MONTH_3: '3mo'
    }
    LIMITS = {
        CandleData.MIN_1: 'max',
        CandleData.MIN_5: 'max',
        CandleData.MIN_15: 'max',
        CandleData.HOUR_1: 'max',
        CandleData.DAY_1: 'max',
        CandleData.WEEK_1: 'max',
        CandleData.MONTH_1: 'max',
        CandleData.MONTH_3: 'max'
    }

    def __init__(self, schema=None, time_zone='Europe/Dublin', df_index=CandleData.DTS):
        """
        Constructor for YahooCandleData

        >>> y = YahooCandleData()
        >>> y = YahooCandleData(schema=[{"name": "open_time", "type": "int64"}, {"name": "open", "type": "float"}])
        >>> y = YahooCandleData(time_zone='Europe/Dublin')

        :param schema: The schema for the candle data.  If None, the default schema is used.
        :param time_zone: The time zone to use for the data.
        :param df_index: The index to use for the dataframe.  If None, the default index is used.
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
        Get the candle data from Yahoo Finance for the given asset and interval.

        >>> y = Yahoo()
        >>> y.get_candles('MSFT', '1d')

        :param symbol: The symbol to fetch.
        :param interval: The interval to fetch.
        :param num_candles: The number of candles to fetch.
        :param start: The start time for a range of candles.
        :param end: The end time for a range of candles.
        """
        self.df = None
        self._set_params(symbol, interval, num_candles=num_candles, start=start, end=end)

        tick = yf.Ticker(self.symbol)
        self.df = tick.history(
            period=self.LIMITS[self.interval],
            interval=self.INTERVALS[self.interval],
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
        """
        Trim the data to the number of candles requested.
        Sometimes the result will be greater than the number of candles requested.
        """
        if self.start and self.end:
            pass
        elif self.start and not self.end:
            self.df = self.df[:min(len(self.df), self.num_candles)]
        else:
            self.df = self.df[max(len(self.df) - self.num_candles, 0):]

if __name__ == '__main__':
    import datetime
    y = YahooCandleData()
    y.get_candles('MSFT', y.MIN_1, end=datetime.datetime.today())
