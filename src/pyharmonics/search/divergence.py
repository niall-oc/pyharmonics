from pyharmonics import constants
from pyharmonics.patterns import Divergence
from pyharmonics.technicals import TechnicalsBase

class DivergenceSearch:
    """
    Search for divergences in the slope of lows or highs.
    """
    HIDDEN = 'Hidden'
    REGULAR = 'Regular'
    EXAGGERATED = 'Exaggerated'
    BULLISH = constants.BULLISH
    BEARISH = constants.BEARISH

    def __init__(self, technicals: TechnicalsBase):
        """
        Constructor for DivergenceSearch.

        >>> d = DivergenceSearch(technicals)

        :param TechnicalsBase technicals: The technicals object to search.
        """
        self.t = technicals
        self.df = technicals.df
        self.found = {self.t.RSI: [], self.t.MACD: []}

    def __exact_dip(self, index, trend, spread):
        """
        Find the local minimum the spread around the index.

        >>> d = DivergenceSearch(technicals)
        >>> d.__exact_dip(100, 'RSI', 20)

        :param int index: The index to search around.
        :param str trend: The trend to search.
        :param int spread: The spread to search.
        :return: The minimum value and index.
        """
        idx = list(range(max(index - spread, 0), min(index + spread, len(self.df))))
        return min(zip(self.df[trend].values[idx], idx))

    def __exact_peak(self, index, trend, spread):
        """
        Find the local maximum the spread around the index.

        >>> d = DivergenceSearch(technicals)
        >>> d.__exact_peak(100, 'RSI', 20)

        :param int index: The index to search around.
        :param str trend: The trend to search.
        :param int spread: The spread to search.
        :return: The maximum value and index.
        """
        idx = list(range(max(index - spread, 0), min(index + spread, len(self.df))))
        return max(zip(self.df[trend].values[idx], idx))

    def __is_bullish(self, start, end, indicator, price, candle_spread):
        """
        Determine if the divergence is bullish.

        >>> d = DivergenceSearch(technicals)
        >>> d.__is_bullish(100, 200, 'RSI', 'LOW', 20)

        :param int start: The start index.
        :param int end: The end index.
        :param str indicator: The indicator to search.
        :param str price: the price trend to search (LOW or HIGH).
        :param int candle_spread: The spread to search.
        """
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
        """
        Determine if the divergence is bearish.

        >>> d = DivergenceSearch(technicals)
        >>> d.__is_bearish(100, 200, 'RSI', 'LOW', 20)

        :param int start: The start index.
        :param int end: The end index.
        :param str indicator: The indicator to search.
        :param str price: The price trend to search (open, low, high, close).
        :param int candle_spread: The spread to search.
        """
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
        Scan for divergences in the slope of a trend.
        Can search for bullish or bearish divergences.

        >>> d = DivergenceSearch(technicals)
        >>> d._search('RSI', 'LOW', 'LOW', d.__is_bullish, 3, 20)

        :param str indicator: The indicator to search.
        :param str peaks: The peaks to search.
        :param str price: The price trend to search (open, low, high, close).
        :param function search_func: The search function to use.
        :param int limit_to: The number of divergences to search for.
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
        Search for divergences in the slope of the lows or highs.

        >>> d = DivergenceSearch(technicals)
        >>> d.search()
        >>> d.search(limit_to=5)

        :param int candle_spread: The spread to search for the divergence.
        :param int limit_to: The number of divergences to search.
        """
        self.found = {self.t.RSI: [], self.t.MACD: []}
        self._search(self.t.RSI, self.t.PRICE_DIPS, constants.LOW, self.__is_bullish, limit_to, candle_spread)
        self._search(self.t.RSI, self.t.PRICE_PEAKS, constants.HIGH, self.__is_bearish, limit_to, candle_spread)
        self._search(self.t.MACD, self.t.PRICE_DIPS, constants.LOW, self.__is_bullish, limit_to, candle_spread)
        self._search(self.t.MACD, self.t.PRICE_PEAKS, constants.HIGH, self.__is_bearish, limit_to, candle_spread)

    def get_patterns(self):
        """
        Return the divergences found.
        """
        return self.found
