from pyharmonics import constants
from pyharmonics.patterns import Divergence
from pyharmonics.technicals import TechnicalsBase

class DivergenceSearch:
    HIDDEN = 'Hidden'
    REGULAR = 'Regular'
    EXAGGERATED = 'Exaggerated'
    BULLISH = constants.BULLISH
    BEARISH = constants.BEARISH

    def __init__(self, technicals: TechnicalsBase):
        """
        """
        self.t = technicals
        self.df = technicals.df
        self.found = {self.t.RSI: [], self.t.MACD: []}

    def __exact_dip(self, index, trend, spread):
        """

        """
        idx = list(range(max(index - spread, 0), min(index + spread, len(self.df))))
        return min(zip(self.df[trend].values[idx], idx))

    def __exact_peak(self, index, trend, spread):
        """

        """
        idx = list(range(max(index - spread, 0), min(index + spread, len(self.df))))
        return max(zip(self.df[trend].values[idx], idx))

    def __is_bullish(self, start, end, indicator, price, candle_spread):
        locater = self.df.iloc
        y1, x1 = self.__exact_dip(start, indicator, candle_spread)
        y2, x2 = self.__exact_dip(end, indicator, candle_spread)
        if y1 < y2 and locater[start][price] >= locater[end][price]:
            # Regular Bullish Divergence
            self.found[indicator].append(Divergence(
                indicator,
                self.REGULAR,
                self.t.get_index_x([start, end]),
                (locater[start][price], locater[end][price],),
                self.t.get_index_x([x1, x2]),
                [y1, y2],
                constants.BULLISH
            ))
        elif y1 > y2 and locater[start][price] < locater[end][price]:
            # hidden Bullish Divergence.
            self.found[indicator].append(Divergence(
                indicator,
                self.HIDDEN,
                self.t.get_index_x([start, end]),
                (locater[start][price], locater[end][price],),
                self.t.get_index_x([x1, x2]),
                [y1, y2],
                constants.BULLISH
            ))
            pass

    def __is_bearish(self, start, end, indicator, price, candle_spread):
        locater = self.df.iloc
        y1, x1 = self.__exact_peak(start, indicator, candle_spread)
        y2, x2 = self.__exact_peak(end, indicator, candle_spread)
        if y1 > y2 and locater[start][price] <= locater[end][price]:
            self.found[indicator].append(Divergence(
                indicator,
                self.REGULAR,
                self.t.get_index_x([start, end]),
                (locater[start][price], locater[end][price],),
                self.t.get_index_x([x1, x2]),
                [y1, y2],
                constants.BEARISH
            ))
        elif y1 < y2 and locater[start][price] > locater[end][price]:
            # hidden Bullish Divergence.
            self.found[indicator].append(Divergence(
                indicator,
                self.HIDDEN,
                self.t.get_index_x([start, end]),
                (locater[start][price], locater[end][price],),
                self.t.get_index_x([x1, x2]),
                [y1, y2],
                constants.BEARISH
            ))

    def _search(self, indicator, peaks, price, search_func, limit_to, candle_spread):
        """
        Scan for divergences in the slope of lows.
        """
        end = -1
        start = -1
        i = len(self.df) - 1
        count = 0
        while i > 0 and count < limit_to:
            if self.df.iloc[i][peaks]:
                if end < 0:
                    end = i
                    i -= 1
                    continue
                else:  # Start and end dips located
                    start = i
                    span_count = 3
                    # walk back 3 peaks
                    while start > 0 and span_count > 0:
                        search_func(start, end, indicator, price, candle_spread)
                        while not self.df.iloc[start][peaks]:
                            start -= 1
                        span_count -= 1
                    end = start
                    start = -1
                count += 1
            i -= 1

    def search(self, candle_spread=20, limit_to=3):
        """
        """
        self.found = {self.t.RSI: [], self.t.MACD: []}
        self._search(self.t.RSI, self.t.PRICE_DIPS, constants.LOW, self.__is_bullish, limit_to, candle_spread)
        self._search(self.t.RSI, self.t.PRICE_PEAKS, constants.HIGH, self.__is_bearish, limit_to, candle_spread)
        self._search(self.t.MACD, self.t.PRICE_DIPS, constants.LOW, self.__is_bullish, limit_to, candle_spread)
        self._search(self.t.MACD, self.t.PRICE_PEAKS, constants.HIGH, self.__is_bearish, limit_to, candle_spread)

    def get_patterns(self):
        return self.found
