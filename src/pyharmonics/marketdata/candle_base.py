#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 17:02:46 2021

@author: xual
"""
import abc
import datetime

class InvalidTimeframe(Exception):
    pass

class CandleData(abc.ABC):
    """
    ALL data apis will convert Kline/candle/trend data into a pandas dataframe.
    This dataframe uses DateTime as the index and
    [OPEN, HIGH, LOW, CLOSE, VOLUME] as column headers.
    """
    DTS = 'dts'
    CLOSE_TIME = 'close_time'
    OPEN = 'open'
    LOW = 'close'
    HIGH = 'high'
    CLOSE = 'close'
    VOLUME = 'volume'
    INDEX = 'index'
    COLUMNS = [OPEN, HIGH, LOW, CLOSE, VOLUME, CLOSE_TIME, DTS]
    MIN_1 = "1m"
    MIN_3 = "3m"
    MIN_5 = "5m"
    MIN_10 = "10m"
    MIN_15 = "15m"
    MIN_30 = "30m"
    MIN_45 = "45m"
    HOUR_1 = "1h"
    HOUR_2 = "2h"
    HOUR_4 = "4h"
    HOUR_8 = "8h"
    DAY_1 = "1d"
    DAY_3 = "3d"
    WEEK_1 = "1w"
    MONTH_1 = "1M"
    MONTH_3 = "3M"
    MONTH_6 = "6M"
    source = None

    def reset_index(self, index=None):
        if index in (self.CLOSE_TIME, self.DTS,):
            self.df_index = index
        self.df[self.INDEX] = self.df[self.df_index]
        self.df = self.df.set_index(self.df[self.INDEX])
        self._set_candle_gap()
        self.df = self.df[self.COLUMNS].drop_duplicates()
        self.df = self.df.sort_index()

    def _set_params(self, symbol, interval, num_candles=None, start=None, end=None):
        """
        Parameters
        ----------
        symbol : str
            The ticker identifier for the asset in question. eg.  'BTCUSDT' or 'META' or 'GOLD'
        interval: str
            eg. '1h' hour, '1m' minute, '1d' day.
        num_candles: int
            The number of candles.  default is 200 candle intervals.
        start: datetime.datetime
            Specific start time for candle data.  This is internally converted into the time format required by Binance
        end: datetime.datetime
            Specific end time for candle data.  This is internally converted into the time format required by Binance
        """
        self.symbol = symbol
        self.interval = interval
        self.num_candles = num_candles or self.MAX_CANDLES
        self.start = start
        self.end = end

    @abc.abstractmethod
    def get_candles(self):
        """
        Set paramaters and convert dates ( especially tricky with binance epoch microseconds. )
        Implement the following
        num_candles      start       end         Expect
        100              None        None        100 candles (finishing at now, end is now)
        100              None        time        100 candles ( finishing at end )
        100              time        None        100 candles ( starting from start )
        100              time        time        candles from start until end ( num_candles is ignored log warning)
        None             None        None        default candles (finishing at now, end is now)
        None             None        time        default candles ( finishing at end )
        None             time        None        default candles ( starting from start )
        None             time        time        candles from start until end ( default is ignored)
        """
        raise NotImplementedError("Specific to api and cannot be general")

    def _datetime_to_epoch(self, t):
        """
        time to epoch in seconds

        Parameters
        ----------
        t : datetime.datetime, int, float, None
            represents time of specific binance candle.

        Returns
        -------
        int

        """
        if t is None:
            return None
        elif isinstance(t, (int, float,)):
            # If an epoch is given with decimals simply cast of the decimals
            return int(t)
        elif isinstance(t, (datetime.date, datetime.datetime,)):
            # Date time must be converted to epoch and bumped up 1000 fold to become milliseconds as required by binance
            return int(t.timestamp())  # type:ignore - can be datetime sometimes
        else:
            raise ValueError('Time must be in datetime or date object')

    def _epoch_to_datetime(self, t):
        """
        epoch in seconds to time

        Parameters
        ----------
        t : datetime.datetime, int, float, None
            represents time of specific binance candle.

        Returns
        -------
        int

        """
        if t is None:
            return None
        elif isinstance(t, (int, float,)):
            # If an epoch is given with decimals simply cast of the decimals
            return datetime.datetime.utcfromtimestamp(int(t))
        elif isinstance(t, (datetime.date, datetime.datetime,)):
            # Date time must be converted to epoch and bumped up 1000 fold to become milliseconds as required by binance
            return t  # type:ignore - can be datetime sometimes
        else:
            raise ValueError('Time must be in epoch')

    def _set_candle_gap(self):
        """
        Calculates the timedelta or epoch between candles.  Important for plotting for this block of data.
        """
        scalar, vector = int(self.interval[:-1]), self.interval[-1:]
        times = {
            'm': {'minutes': scalar},
            'h': {'hours': scalar},
            'd': {'days': scalar},
            'w': {'days': scalar * 7},
            'M': {'days': scalar * 30}
        }
        kwargs = times[vector]
        self.candle_gap = datetime.timedelta(**kwargs)

        # in the case of the df_index being epoch the x on a pattern or plot will be measured in epoch too.
        if self.df_index == self.CLOSE_TIME:
            now = datetime.datetime.now()
            then = now - self.candle_gap
            self.candle_gap = int(now.timestamp() - then.timestamp())
