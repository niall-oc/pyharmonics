
__author__ = 'github.com/niall-oc'

from ta.trend import MACD, SMAIndicator, EMAIndicator
from ta.momentum import RSIIndicator, StochRSIIndicator
from ta.volatility import BollingerBands
from pyharmonics import constants, utils
import numpy as np
import math
import abc


class TechnicalsBase(abc.ABC):
    """
    ALL candle data apis convert Kline or trend data into a pandas dataframe.
    The market_data dataframe uses DateTime as the index and
    [OPEN, HIGH, LOW, CLOSE, VOLUME] as column headers.

    Every pattern that indicates a bullish or bearish entry ( buy or sell )
    Is based on both the price, volume and indicator analyses.

    Peaks, indicators and fibonacci matrix are extended on to candle data.
    Candle data is a parameter to this constructor
    """
    TREND = 'trend'
    PEAK = 'peak'
    PEAK_PRICE = 1
    PEAK_INDEX = 0
    PEAK_TYPE = 2

    RSI = "rsi"
    MACD = "macd"
    MFI = "mfi"
    CCI = "cci"
    STOCH_RSI = 'stoch_rsi'
    BBP = 'bb%'
    ADX = 'adx'
    DIm = 'di-'
    DIp = 'di+'
    OBS = "obs"
    HIGHS = 'highs'
    LOWS = 'lows'

    EMA_5 = "ema 5"
    EMA_8 = "ema 8"
    EMA_13 = "ema_13"
    EMA_21 = "ema 21"
    EMA_34 = "ema 34"
    EMA_55 = "ema 55"

    SMA_50 = "sma 50"
    SMA_100 = "sma 100"
    SMA_200 = "sma 200"
    SMA_150 = "sma 150"

    # Divergences
    DIVERGENCE = 'divergence'
    REGULAR = 'regular'
    EXEGGERATED = 'exeggerated'
    HIDDEN = 'hidden'

    # Peaks
    PRICE_PEAKS = 'price_peaks'
    PRICE_DIPS = 'price_dips'
    MACD_PEAKS = 'macd_peaks'
    MACD_DIPS = 'macd_dips'
    RSI_PEAKS = 'rsi_peaks'
    RSI_DIPS = 'rsi_dips'
    STOCH_RSI_PEAKS = 'stoch_rsi_peaks'
    STOCH_RSI_DIPS = 'stoch_rsi_dips'

    def __init__(self, df, indicator_config=None, sma_config=None, ema_config=None, peak_spacing=10):
        """
        Parameters
        ----------
        df: pandas.DataFrame
            Must contain ['open', 'high', 'close', 'low', 'volume']
        indicator_config : dict
            kw arguments for techincal indicators, stoch_rsi, rsi, mfi, cci and macd implemented
            defaults are  {
                Technicals.MACD: {'window_slow': 26, 'window_fast': 12, 'window_sign': 9},
                Technicals.STOCH_RSI: {'window': 14, 'smooth_window': 3},
                Technicals.RSI: {'window': 14},
                Technicals.CCI: {'window': 20, 'constant': 0.015},
                Technicals.MFI: {'window': 20}
            }
        sma_config: dict
            kw arguments for simple moving averages.
            defaults are {
                self.SMA_50: {'window': 50},
                self.SMA_100: {'window': 100},
                self.SMA_150: {'window': 150},
                self.SMA_200: {'window': 200}
            }
        ema_config: dict
            kw arguments for exponential moving averages.
            defaults are {
                self.EMA_5: {'window': 5},
                self.EMA_8: {'window': 8},
                self.EMA_13: {'window': 13},
                self.EMA_21: {'window': 21},
                self.EMA_34: {'window': 34},
                self.EMA_55: {'window': 55}
            }
        peak_spacing: int
            higher number means less sensitivity to peaks.

        returns
        -------
        None
        """
        self.INDICATOR_CONFIG = indicator_config or {
            self.MACD: {'window_slow': 26, 'window_fast': 12, 'window_sign': 9},
            self.RSI: {'window': 14},
            self.STOCH_RSI: {'window': 14},
            self.BBP: {'window': 20, 'window_dev': 2}
        }
        self.SMA_CONFIG = sma_config or {
            self.SMA_50: {'window': 50},
            self.SMA_100: {'window': 100},
            self.SMA_150: {'window': 150},
            self.SMA_200: {'window': 200}
        }
        self.EMA_CONFIG = ema_config or {
            self.EMA_5: {'window': 5},
            self.EMA_8: {'window': 8},
            self.EMA_13: {'window': 13},
            self.EMA_21: {'window': 21},
            self.EMA_34: {'window': 34},
            self.EMA_55: {'window': 55}
        }
        self.df = df.copy()
        self.peak_spacing = peak_spacing
        self.interval_map = {
            constants.WEEK_1: math.ceil(math.log(1) * 10),
            constants.DAY_1: math.ceil(math.log(1) * 10),
            constants.HOUR_8: math.ceil(math.log(3) * 10),
            constants.HOUR_4: math.ceil(math.log(6) * 8),
            constants.HOUR_2: math.ceil(math.log(12) * 6),
            constants.HOUR_1: math.ceil(math.log(24) * 6),
            constants.MIN_45: math.ceil(math.log(32) * 5),
            constants.MIN_30: math.ceil(math.log(48) * 4),
            constants.MIN_15: math.ceil(math.log(96) * 4),
            constants.MIN_5: math.ceil(math.log(288) * 3),
            constants.MIN_1: math.ceil(math.log(1440) * 2)
        }
        if self.df is None:
            raise ValueError('Candle DataFrame is None! call cd.get_candles(ASSET, INTERVAL) first.')
        elif not len(self.df):
            raise IndexError("Candle DataFrame is empty")

    def _set_peak_data(self):
        """
        Sets peak spacing for this objects and finds peak data on indicators and prices.
        Builds Fibonacci matrix based on price peak data.
        """
        self._set_indicators()
        self._set_moving_avergaes()

        for indicator, trend in self.indicators.items():
            self.df[indicator] = trend

        for key in self.SMA_CONFIG:
            self.df[key] = self.smas[key].sma_indicator()

        for key in self.EMA_CONFIG:
            self.df[key] = self.emas[key].ema_indicator()

        self._build_peaks()
        # self._build_peak_slopes()
        self.spot = self.df[constants.CLOSE].iloc[-1]

    def _build_peaks(self):
        """

        Parameters
        ----------
        peak_spacing : int, optional
            Helps argelextrema find true peaks and removes noise. The default is 10.

        Returns
        -------
        list of tuples, peak_idx, peak_price

        """
        self.df[self.MACD_PEAKS] = np.int64(utils.find_peaks(self.indicators[self.MACD].values, np.greater_equal, order=self.peak_spacing))
        self.df[self.MACD_DIPS] = np.int64(utils.find_peaks(self.indicators[self.MACD].values, np.less_equal, order=self.peak_spacing))
        self.df[self.RSI_PEAKS] = np.int64(utils.find_peaks(self.indicators[self.RSI].values, np.greater_equal, order=self.peak_spacing))
        self.df[self.RSI_DIPS] = np.int64(utils.find_peaks(self.indicators[self.RSI].values, np.less_equal, order=self.peak_spacing))
        # Special case to remove false peaks and dips in MACD readings.
        self.df[self.MACD_PEAKS] = self.df.apply(lambda row: np.int64(row[self.MACD] >= 0 and row[self.MACD_PEAKS] > 0), axis=1)
        self.df[self.MACD_DIPS] = self.df.apply(lambda row: np.int64(row[self.MACD] < 0 and row[self.MACD_DIPS] > 0), axis=1)

        self.highs, y = self.get_peak_x_y(self.PRICE_PEAKS)
        self.peak_data = [
            (index, price, 1)
            for index, price in zip(self.highs, y)
        ]
        self.lows, y = self.get_peak_x_y(self.PRICE_DIPS)
        self.peak_data += [
            (index, price, 0)
            for index, price in zip(self.lows, y)
        ]
        self.peak_data = sorted(self.peak_data, key=lambda x: x[0])

        # Calculate peak info
        self.peak_indexes = [p[0] for p in self.peak_data]
        self.peak_prices = [p[1] for p in self.peak_data]
        self.peak_type = [p[2] for p in self.peak_data]

        self.peak_indicators = {
            self.MACD: {
                constants.BULLISH: self.df[self.MACD_DIPS],
                constants.BEARISH: self.df[self.MACD_PEAKS],
            },
            self.RSI: {
                constants.BULLISH: self.df[self.RSI_DIPS],
                constants.BEARISH: self.df[self.RSI_PEAKS],
            }
        }

    def _set_moving_avergaes(self):
        self.smas = {}
        for ma, config in self.SMA_CONFIG.items():
            self.smas[ma] = SMAIndicator(close=self.df[constants.CLOSE], **config)
        self.emas = {}
        for ma, config in self.EMA_CONFIG.items():
            self.emas[ma] = EMAIndicator(close=self.df[constants.CLOSE], **config)

    def _set_indicators(self):
        self.indicators = {
            self.MACD: MACD(close=self.df[constants.CLOSE], **self.INDICATOR_CONFIG[self.MACD]).macd_diff(),
            self.RSI: RSIIndicator(close=self.df[constants.CLOSE], **self.INDICATOR_CONFIG[self.RSI]).rsi(),
            self.STOCH_RSI: StochRSIIndicator(close=self.df[constants.CLOSE], **self.INDICATOR_CONFIG[self.STOCH_RSI]).stochrsi_d(),
            self.BBP: BollingerBands(close=self.df[constants.CLOSE], **self.INDICATOR_CONFIG[self.BBP]).bollinger_pband()
        }

    @abc.abstractmethod
    def get_peak_x_y(self):
        pass

    def get_index_x(self, x):
        """
        Resolve the index of a pattern into an actual dataframe index ( epoch or date time stam ( dts ))

        >>> t = OHLCTechnicals(df, symbol, time_frame)
        >>> t.get_index_x([1, 2, 3])
        [Timestamp('2023-04-17 08:59:59+0100', tz='Europe/Dublin'),
         Timestamp('2023-04-17 12:59:59+0100', tz='Europe/Dublin'),
         Timestamp('2023-04-17 16:59:59+0100', tz='Europe/Dublin')]
        """
        return list(self.df.index[x])

    def get_pattern_x_y(self, peak_indexes):
        """
        Given the indexs of a pattern ( not a dataframe ) found in this technical data,
        return the time and prices at those indexes.

        Parameters
        ----------
        pattern_indexes: list
            The indexes within technical_data.peak_indexes and technical_data.peak_prices that form the pattern.

        >>> t.get_pattern_x_y([1, 2, 3])
        ([29, 42, 46], [27125.0, 28000.0, 26942.82])
        """
        x = [self.peak_indexes[i] for i in peak_indexes]
        y = [self.peak_prices[i] for i in peak_indexes]
        return x, y

    def get_series_x_y(self, series_indexes, series):
        """
        Given the indexs of a pattern found in this technical data,
        return the time and indicator readings at those indexes.

        Parameters
        ----------
        pattern_indexes: list
            The indexes within technical_data.peak_indexes and technical_data.peak_prices that form the pattern.

        >>> t.get_series_x_y([100, 200, 300], t.MACD)
        ([100, 200, 300], [5.503533503855266, -11.21857793005239, -160.57022744782142])
        """
        y = list(self.df[series].values[series_indexes])
        return series_indexes, y

    def filter_peak_data(self, lows=False):
        """
        Extract either the highs or the lows from peaks.

        >>> t.filter_peak_data()
        [(9, 30485.0, 1), (42, 28000.0, 1), (57, 30036.0, 1), (81, 29969.39, 1), ...]
        >>> t.filter_peak_data(lows=True)
        [(29, 27125.0, 0), (46, 26942.82, 0), (89, 27666.95, 0), (131, 27262.0, 0), ...]
        """
        if lows:
            # return lows - PEAK_TYPE = 0
            return [i for i in self.peak_data if not i[self.PEAK_TYPE]]
        else:
            # return lows - PEAK_TYPE = 1
            return [i for i in self.peak_data if i[self.PEAK_TYPE]]

    def _build_peak_slopes(self):
        """
        Calculate slopes for peaks.
        """
        DF_LEN = len(self.df)

        # Trend low peak slopes
        price_low_slopes = [None] * DF_LEN
        lows = self.filter_peak_data(lows=True)
        for i in range(1, len(lows)):
            price_low_slopes[lows[i][self.PEAK_INDEX]] = utils.line_slope(
                lows[i][self.PEAK_PRICE], lows[i - 1][self.PEAK_PRICE],
                lows[i][self.PEAK_INDEX], lows[i - 1][self.PEAK_INDEX]
            )

        self.reverse_fill_na(price_low_slopes, limit_index=self.lows[0])

        # Trend high peak slopes
        price_high_slopes = [None] * DF_LEN
        highs = self.filter_peak_data(lows=False)
        for i in range(1, len(highs)):
            price_high_slopes[highs[i][self.PEAK_INDEX]] = utils.line_slope(
                highs[i][self.PEAK_PRICE], highs[i - 1][self.PEAK_PRICE],
                highs[i][self.PEAK_INDEX], highs[i - 1][self.PEAK_INDEX]
            )
        self.reverse_fill_na(price_high_slopes, limit_index=self.highs[0])

        self.divergences = {}
        for ind, peaks in self.peak_indicators.items():
            self.divergences[ind] = {}
            for is_bullish, indexes in peaks.items():
                # get readings
                x, ind_values = self.get_series_x_y(indexes, ind)
                # measure slopes
                this_trend = [None] * DF_LEN
                for i in range(1, len(indexes)):
                    this_trend[indexes[i]] = utils.line_slope(ind_values[i], ind_values[i - 1], indexes[i], indexes[i - 1])
                self.reverse_fill_na(this_trend, limit_index=indexes[0])
                # check divergences
                # None means nothing is diverging
                self.divergences[ind][is_bullish] = [0] * DF_LEN
                slopes = price_low_slopes if is_bullish else price_high_slopes
                for i in range(DF_LEN):
                    # if nothing to compare, or both slopes moving in the same direction
                    if slopes[i] is None or this_trend[i] is None or\
                       (slopes[i] > 0.0 and this_trend[i] > 0.0) or (slopes[i] < 0.0 and this_trend[i] < 0.0):
                        continue
                    else:
                        # If slopes are not running in the same direction there is a divergence
                        # The is_bullish flag indicates the direction of the divergence ie. bullish or
                        self.divergences[ind][is_bullish][i] = 1
        return None


class OHLCTechnicals(TechnicalsBase):
    def __init__(self, df, symbol, interval, indicator_config=None, sma_config=None, ema_config=None, peak_spacing=10):
        super(OHLCTechnicals, self).__init__(df, indicator_config=indicator_config, sma_config=sma_config, peak_spacing=peak_spacing)
        self.symbol = symbol
        self.interval = interval
        self.df[self.PRICE_PEAKS] = np.int64(utils.find_peaks(self.df[constants.HIGH].values, np.greater_equal, order=self.peak_spacing))
        self.df[self.PRICE_DIPS] = np.int64(utils.find_peaks(self.df[constants.LOW].values, np.less_equal, order=self.peak_spacing))
        self._set_peak_data()

    def get_peak_x_y(self, peak_type):
        """
        Given the indexs of a pattern ( not a dataframe ) found in this technical data,
        return the time and prices at those indexes.

        Parameters
        ----------
        peak_type: str
            The series containing True or False where True marks a peak on this trend

        """
        x = np.nonzero(self.df[peak_type].values)[0]
        if peak_type == self.PRICE_PEAKS:
            y = self.df[constants.HIGH].values[x]
        elif peak_type == self.PRICE_DIPS:
            y = self.df[constants.LOW].values[x]
        elif peak_type == self.MACD_PEAKS or peak_type == self.MACD_DIPS:
            y = self.df[self.MACD].values[x]
        elif peak_type == self.RSI_PEAKS or peak_type == self.RSI_DIPS:
            y = self.df[self.RSI].values[x]
        else:
            raise ValueError('Unknown peak type requested')
        return x, y

class Technicals(TechnicalsBase):
    def __init__(self, df, symbol, interval, indicator_config=None, sma_config=None, ema_config=None, peak_spacing=10):
        super(Technicals, self).__init__(df, indicator_config=indicator_config, sma_config=sma_config, peak_spacing=peak_spacing)
        self.symbol = symbol
        self.interval = interval
        self.df[self.PRICE_PEAKS] = np.int64(utils.find_peaks(self.df[constants.CLOSE].values, np.greater_equal, order=self.peak_spacing))
        self.df[self.PRICE_DIPS] = np.int64(utils.find_peaks(self.df[constants.CLOSE].values, np.less_equal, order=self.peak_spacing))
        self._set_peak_data()

    def get_peak_x_y(self, peak_type):
        """
        Given the indexs of a pattern ( not a dataframe ) found in this technical data,
        return the time and prices at those indexes.

        Parameters
        ----------
        peak_type: str
            The series containing True or False where True marks a peak on this trend

        """
        x = np.nonzero(self.df[peak_type].values)[0]
        if peak_type == self.PRICE_PEAKS:
            y = self.df[constants.CLOSE].values[x]
        elif peak_type == self.PRICE_DIPS:
            y = self.df[constants.CLOSE].values[x]
        elif peak_type == self.MACD_PEAKS or peak_type == self.MACD_DIPS:
            y = self.df[self.MACD].values[x]
        elif peak_type == self.RSI_PEAKS or peak_type == self.RSI_DIPS:
            y = self.df[self.RSI].values[x]
        else:
            raise ValueError('Unknown peak type requested')
        return x, y
