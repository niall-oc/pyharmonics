from pyharmonics.marketdata.candle_base import CandleData, InvalidTimeframe
import pandas as pd
from binance.spot import Spot
import datetime

class BinanceCandleData(CandleData):
    """
    If you want to get market data or prices for crypto currencies, you can use this class.
    This class is a subclass of CandleData and is used to get candle data from Binance.

    >>> m = BinanceCandleData() # create a new instance of BinanceCandleData

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
    SOURCE = 'Binance'
    INTERVALS = {
        CandleData.MIN_1: '1m',
        CandleData.MIN_3: '3m',
        CandleData.MIN_5: '5m',
        CandleData.MIN_15: '15m',
        CandleData.MIN_30: '30m',
        CandleData.MIN_45: '45m',
        CandleData.HOUR_1: '1h',
        CandleData.HOUR_2: '2h',
        CandleData.HOUR_4: '4h',
        CandleData.HOUR_8: '8h',
        CandleData.DAY_1: '1d',
        CandleData.DAY_3: '3d',
        CandleData.WEEK_1: '1w',
        CandleData.MONTH_1: '1M'
    }

    def __init__(self, schema=None, time_zone='Europe/Dublin', df_index=CandleData.DTS):
        """
        Constructor for BinanceCandleData

        :param schema: The schema for the candle data.  If None, the default schema is used.
        :param time_zone: The time zone to use for the data.
        :param df_index: The index to use for the dataframe.  If None, the default index is used.
        """
        # Binance returns a list of lists. There is no schema as such and typing must be defined in line with biances API.
        # Making the schema a paramater means it can be updated using a config and no code change.
        # Data types are pandas series data types.
        if schema is None:
            self.schema = [
                {"name": "open_time", "type": "int64"},
                {"name": self.OPEN, "type": "float"},
                {"name": self.HIGH, "type": "float"},
                {"name": self.LOW, "type": "float"},
                {"name": self.CLOSE, "type": "float"},
                {"name": self.VOLUME, "type": "float"},
                {"name": self.CLOSE_TIME, "type": "int64"},
                {"name": "quote_asset_volume", "type": "float"},
                {"name": "number_of_trades", "type": "int64"},
                {"name": "taker_base_asset_volume", "type": "float"},
                {"name": "taker_quote_asset_colume", "type": "float"},
                {"name": "ignore", "type": "float"}
            ]

        self.columns = [c['name'] for c in self.schema]
        # Binance can be queried for read only operations without an API key.
        self.rc = Spot(api_key=None, api_secret=None)
        # time zone reflects must be set to correct region otherwise patern detection may produce strange time points.
        self.time_zone = time_zone
        self.df = None
        self.candle_gap = None
        if df_index in (self.DTS, self.CLOSE_TIME):
            self.df_index = df_index
        else:
            raise ValueError(f'df_index must be one of "{self.DTS}" or "{self.CLOSE_TIME}"')

    def _to_dataframe(self, row_data):
        """
        Converts the raw data from the API into a pandas dataframe.

        :param row_data: The raw data from the API.
        :return: The pandas dataframe
        """
        df = pd.DataFrame(data=row_data, columns=self.columns)

        for col in self.schema:
            df[col['name']] = df[col['name']].astype(col['type'])

        df[self.CLOSE_TIME] = df[self.CLOSE_TIME].map(lambda x: int(x / 1000))   # binance epoch is millisecond
        df[self.DTS] = pd.to_datetime(df[self.CLOSE_TIME], unit='s', utc=True).dt.tz_convert(self.time_zone)
        return df[self.COLUMNS]  # Hold on to only the essentials and save memory

    def _datetime_to_epoch(self, t):
        """
        Overridden method to convert a datetime object to an epoch time.
        Binance requires epoch time in milliseconds.

        >>> m._datetime_to_epoch(datetime.datetime(2020, 3, 21, 14, 0, 15))
        1584801615000

        :param t: The datetime object to convert.
        :return: The epoch time.
        """
        epoch = super()._datetime_to_epoch(t)
        if isinstance(epoch, (int, float)):
            epoch = int(epoch)
            if len(str(epoch)) < 11:
                epoch = int(epoch * 1000)
        return epoch

    def _epoch_to_datetime(self, t):
        """
        Overridden method to convert an epoch time to a datetime object.
        Binance requires epoch time in milliseconds.

        >>> m._epoch_to_datetime(1584801615000)
        datetime.datetime(2020, 3, 21, 14, 0, 15)

        :param t: The epoch time to convert.
        :return: The datetime object.
        """
        if isinstance(t, (int, float)):
            epoch = int(t)
            if len(str(epoch)) > 10:
                t = t / 1000
        return super()._epoch_to_datetime(epoch)

    def get_candles(self, symbol, interval, num_candles=None, start=None, end=None):
        """
        If start and end are defined all candles between those time ranges will be pulled
        and stored in self.df.  This is done using multiple calls.
        This is done in blocks of 1000 candles.

        If only start or end or both are None, then a single call is made.
        If num_candles is greater than 1000 then multiple calls are made to get the data.

        >>> m.get_candles('BTCUSDT', '1h', num_candles=1000)
        >>> m.get_candles('BTCUSDT', '1h', num_candles=1000, end=datetime.datetime(2020, 3, 21, 14, 0, 15))
        >>> m.get_candles('BTCUSDT', '1h', num_candles=1000, start=datetime.datetime(2020, 3, 21, 14, 0, 15))
        >>> m.get_candles('BTCUSDT', '1h', start=datetime.datetime(2020, 3, 21, 14, 0, 15))

        :param symbol: The symbol to fetch.
        :param interval: The interval to fetch.
        :param num_candles: The number of candles to fetch.
        :param start: The start time for a range of candles.
        :param end: The end time for a range of candles.
        """
        self.df = None
        row_data = []
        if interval not in self.INTERVALS:
            raise InvalidTimeframe(f"Binance timeframe intervals must be one of {self.INTERVALS}")

        self._set_params(symbol, interval, num_candles=num_candles, start=start, end=end)
        # Start and end are explicit.

        if self.start and self.end:
            start_index = self.start
            end_index = self.end
            while start_index <= end_index:
                block_data = self._get_candle_block(end=end_index)
                if len(block_data) < 2:
                    break
                end_index = block_data[0][0]
                row_data += block_data
            block_data = self._get_candle_block()
        elif self.num_candles > self.MAX_CANDLES:
            candles_remaining = self.num_candles
            time_index = self._datetime_to_epoch(self.end or datetime.datetime.now())
            while candles_remaining > 0:
                block_data = self._get_candle_block(end=time_index, num_candles=min(self.MAX_CANDLES, candles_remaining))
                if len(block_data) < 2:
                    break
                time_index = block_data[0][0]
                candles_remaining -= len(block_data)
                row_data += block_data
        else:
            # Start + num_candles  OR (end OR now ) - num_candles is returned
            row_data = self._get_candle_block(start=self.start, end=self.end, num_candles=self.num_candles)
        self.df = self._to_dataframe(row_data)
        row_data = None
        self.reset_index()

    def _set_params(self, symbol, interval, num_candles=None, start=None, end=None):
        """
        Set the parameters for the candle data. These are used to fetch the data from the source.

        :param symbol: The symbol to fetch.
        :param interval: The interval to fetch.
        :param num_candles: The number of candles to fetch.
        :param start: The start time for a range of candles.
        :param end: The end time for a range of candles.
        """
        self.symbol = symbol
        self.interval = interval
        self.num_candles = num_candles or self.MAX_CANDLES
        self.start = self._datetime_to_epoch(start)
        self.end = self._datetime_to_epoch(end)

    def _get_candle_block(self, start=None, end=None, num_candles=None):
        """
        Calls binance API to get a block of candle data.

        >>> m._get_candle_block(start=datetime.datetime(2020, 3, 21, 14, 0, 15))
        >>> m._get_candle_block(end=datetime.datetime(2020, 3, 21, 14, 0, 15))
        >>> m._get_candle_block(num_candles=1000)

        :param start: The start time for a range of candles.
        :param end: The end time for a range of candles.
        :param num_candles: The number of candles to fetch.
        :return: The data from the API.
        """
        limit = num_candles

        data = self.rc.klines(
            self.symbol,
            self.INTERVALS[self.interval],
            startTime=start,
            endTime=end,
            limit=limit
        )
        return data

if __name__ == '__main__':
    # Debugging
    b = BinanceCandleData()
    start = datetime.datetime(2021, 8, 28, 23, 59, 59)
    b.get_candles('MATICUSDT', b.DAY_1, start=start)
