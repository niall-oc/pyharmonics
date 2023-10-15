#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 17:02:46 2021

@author: xual
"""
import abc
import datetime
from pyharmonics import constants

class InvalidTimeframe(Exception):
    pass

class CandleData(abc.ABC):
    """
    ALL data apis will convert Kline/candle/trend data into a pandas dataframe.
    This dataframe uses DateTime as the index and
    [OPEN, HIGH, LOW, CLOSE, VOLUME] as column headers.
    """
    DTS = constants.DTS
    CLOSE_TIME = constants.CLOSE_TIME
    OPEN = constants.OPEN
    LOW = constants.LOW
    HIGH = constants.HIGH
    CLOSE = constants.CLOSE
    VOLUME = constants.VOLUME
    INDEX = constants.INDEX
    COLUMNS = [OPEN, HIGH, LOW, CLOSE, VOLUME, CLOSE_TIME, DTS]
    MIN_1 = constants.MIN_1
    MIN_3 = constants.MIN_3
    MIN_5 = constants.MIN_5
    MIN_10 = constants.MIN_10
    MIN_15 = constants.MIN_15
    MIN_30 = constants.MIN_30
    MIN_45 = constants.MIN_45
    HOUR_1 = constants.HOUR_1
    HOUR_2 = constants.HOUR_2
    HOUR_4 = constants.HOUR_4
    HOUR_8 = constants.HOUR_8
    DAY_1 = constants.DAY_1
    DAY_3 = constants.DAY_3
    DAY_5 = constants.DAY_5
    WEEK_1 = constants.WEEK_1
    MONTH_1 = constants.MONTH_1
    MONTH_3 = constants.MONTH_3
    MONTH_6 = constants.MONTH_6
    SOURCE = None

    def reset_index(self, index=None):
        if index in (self.CLOSE_TIME, self.DTS,):
            self.df_index = index
        self.df[self.INDEX] = self.df[self.df_index]
        self.df = self.df.set_index(self.df[self.INDEX])
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
