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
        idx = list(range(index - spread, index + spread))
        return min(zip(self.df[trend].values[idx], idx))[1]

    def __exact_peak(self, index, trend, spread):
        """

        """
        idx = list(range(index - spread, index + spread))
        return max(zip(self.df[trend].values[idx], idx))[1]

    def __is_bullish(self, start, end, indicator, price, candle_spread):
        locater = self.df.iloc
        x = self.t.get_index_x([start, end])
        if locater[start][indicator] < locater[end][indicator] and locater[start][price] >= locater[end][price]:
            # Regular Bullish Divergence
            self.found[indicator].append(Divergence(
                indicator,
                self.REGULAR,
                x,
                (locater[start][price], locater[end][price],),
                x,
                (locater[start][indicator], locater[end][indicator],),
                constants.BULLISH
            ))
        elif locater[start][indicator] > locater[end][indicator] and locater[start][price] < locater[end][price]:
            # hidden Bullish Divergence.
            self.found[indicator].append(Divergence(
                indicator,
                self.HIDDEN,
                x,
                (locater[start][price], locater[end][price],),
                x,
                (locater[start][indicator], locater[end][indicator],),
                constants.BULLISH
            ))
            pass

    def __is_bearish(self, start, end, indicator, price, candle_spread):
        locater = self.df.iloc
        x = self.t.get_index_x([start, end])
        if locater[start][indicator] > locater[end][indicator] and locater[start][price] <= locater[end][price]:
            self.found[indicator].append(Divergence(
                indicator,
                self.REGULAR,
                x,
                (locater[start][price], locater[end][price],),
                x,
                (locater[start][indicator], locater[end][indicator],),
                constants.BEARISH
            ))
        elif locater[start][indicator] < locater[end][indicator] and locater[start][price] > locater[end][price]:
            # hidden Bullish Divergence.
            self.found[indicator].append(Divergence(
                indicator,
                self.HIDDEN,
                x,
                (locater[start][price], locater[end][price],),
                x,
                (locater[start][indicator], locater[end][indicator],),
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
                    search_func(start, end, indicator, price, candle_spread)
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
