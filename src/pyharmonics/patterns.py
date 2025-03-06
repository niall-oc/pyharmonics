__author__ = 'github.com/niall-oc'

import abc
from pyharmonics import constants
from hashlib import sha256

class HarmonicPattern(abc.ABC):
    """
    A base class for all harmonic patterns.

    A harmonic pattern is one from price swings that retrace to fibonacci levels.

    ABCD, XABCD ( Gartley, Bat, Butterfly, Crab, Cypher, Shark, 5-0, etc. )
    """
    @abc.abstractmethod
    def to_dict(self):
        raise NotImplementedError


class ABCPattern(HarmonicPattern):
    """
    An extension of the HarmonicPattern class for ABC patterns.

    ABC patterns are a subset of harmonic patterns that have a 2 swing structure.
    A price moves in an up or down swing and retraces to a fibonacci level before
    continuing in the original direction.

    .382, .5, .618, .786, .886, 1.13, 1.141, 1.618 are common retracement levels.
    """
    def __init__(
        self,
        symbol,
        interval,
        x: tuple,
        y: tuple,
        name: str,
        retraces: dict,
        formed: bool,
        bullish: bool
    ):
        """
        Constructor for ABCPattern.

        >>> p = ABCPattern('BTCUSDT', '1h', (1, 2), (3, 4), 'Gartley', {0.382: 1, 0.618: 2}, True, True)

        :param str symbol: The symbol for the pattern.
        :param str interval: The interval for the pattern.
        :param tuple x: The x points for the pattern.
        :param tuple y: The y points for the pattern.
        :param str name: The name of the pattern.
        :param dict retraces: retraces are calculated from the y points.
        :param bool formed: True if the pattern is formed.
        :param bool bullish: True if the pattern is bullish.
        """
        self.symbol = symbol
        self.interval = interval
        self.x = x
        self.y = y
        self.name = name
        self.retraces = retraces
        self.formed = formed
        self.bullish = bullish
        self._set_completion_price()
        self._set_CD_leg_extensions()
        # Edge case when stocks are near bust!
        self.hop = max(self.hop, 0.0)
        self.completion_min_price = max(self.completion_min_price, 0.0)
        self.completion_max_price = max(self.completion_max_price, 0.0)
        self._set_hash()

    def to_dict(self):
        """
        Return a dictionary representation of the pattern.
        """
        return dict(
            symbol=self.symbol,
            interval=self.interval,
            name=self.name,
            formed=self.formed,
            retraces=self.retraces,
            bullish=self.bullish,
            x=self.x,
            y=self.y,
            abc_extensions=self.abc_extensions,
            completion_min_price=self.completion_min_price,
            completion_max_price=self.completion_max_price,
        )

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        args = [f'{k}={repr(v)}' for k, v in self.to_dict().items()]
        return f"{self.__class__.__name__}({', '.join(args)})"

    def _set_hash(self):
        """
        Set a unique pattern id for this pattern.
        """
        seed = f"{self.bullish}{self.name}{self.x[:-2]}{self.y[:-2]}{self.completion_min_price}{self.completion_max_price}"
        self.p_id = sha256(seed.encode()).hexdigest()

    def _set_CD_leg_extensions(self):
        """
        Using the ABC component of a pattern, calculate the BC leg projection and extension levels.
        """
        C = self.y[-1]
        self.abc_extensions = [C]
        self.hop = C

    def _set_completion_price(self):
        """
        Calculates the completion price range for this pattern based off the XAB or XCD pattern completion retrace.
        """
        C = self.y[-1]
        self.completion_min_price = C
        self.completion_max_price = C

class ABCDPattern(ABCPattern):
    """
    An extension of the ABCPattern class for ABCD patterns.

    ABCD patterns are a subset of harmonic patterns that have a 3 swing structure.
    A price moves in an up or down swing and retraces to a fibonacci level before
    continuing in the opposite direction.
    """
    def _set_completion_price(self):
        """
        Calculates the completion price range for this pattern based off the XAB or XCD pattern completeion retrace.
        """
        B = self.y[-3]
        C = self.y[-2]
        abcd_retraces = constants.MATRIX_PATTERNS[constants.ABCD][self.name]
        if self.bullish:
            self.completion_min_price = C - ((C - B) * abcd_retraces[constants.MIN])
            self.completion_max_price = C - ((C - B) * abcd_retraces[constants.MAX])
        else:
            self.completion_min_price = C + ((B - C) * abcd_retraces[constants.MIN])
            self.completion_max_price = C + ((B - C) * abcd_retraces[constants.MAX])

    def __repr__(self):
        args = [f'{k}={repr(v)}' for k, v in self.to_dict().items()]
        return f"{self.__class__.__name__}({', '.join(args)})"

class XABCDPattern(ABCPattern):
    """
    An extension of the ABCPattern class for XABCD patterns.

    XABCD patterns are a subset of harmonic patterns that have a 4 swing structure.
    A price moves in an up or down swing and retraces to a fibonacci level before
    continuing in the opposite direction.
    """
    def _set_completion_price(self):
        """
        Calculates the completion price range for this pattern based off the XAB or XCD pattern completeion retrace.
        """
        X = self.y[0]
        A = self.y[1]
        C = self.y[3]
        peak_price = C if C > A else A
        completion_retraces = constants.MATRIX_PATTERNS[constants.XABCD][self.name]
        if self.bullish:
            self.completion_min_price = peak_price - ((peak_price - X) * completion_retraces[constants.MIN])
            self.completion_max_price = peak_price - ((peak_price - X) * completion_retraces[constants.MAX])

        else:
            self.completion_min_price = peak_price + ((X - peak_price) * completion_retraces[constants.MIN])
            self.completion_max_price = peak_price + ((X - peak_price) * completion_retraces[constants.MAX])

    def _set_CD_leg_extensions(self):
        """
        Using the ABC component of a pattern, calculate the CD leg projection and extension levels.
        """
        A = self.y[-4]
        B = self.y[-3]
        C = self.y[-2]
        move = abs(A - B)

        ext = [e for e in sorted(constants.ABC_EXTENSIONS)]
        if self.bullish:
            self.abc_extensions = [C - (e * move) for e in ext]
            # self.hop = self.abc_extensions[-1]
            for e in self.abc_extensions:
                if e < self.completion_max_price:
                    self.hop = e
                    break
        else:
            self.abc_extensions = [C + (e * move) for e in ext]
            # self.hop = self.abc_extensions[-1]
            for e in self.abc_extensions:
                if e > self.completion_max_price:
                    self.hop = e
                    break

    def __repr__(self):
        args = [f'{k}={repr(v)}' for k, v in self.to_dict().items()]
        return f"{self.__class__.__name__}({', '.join(args)})"

class Divergence:
    """
    A class to represent a divergence pattern in the market.

    A divergence is a disagreement between the price and an indicator.
    While the price makes a new high or low, the indicator does not.
    """
    def __init__(
        self,
        indicator: str,
        name: str,
        x: tuple,
        y: tuple,
        ind_x: tuple,
        ind_y: tuple,
        bullish: bool
    ):
        """
        Constructor for Divergence.

        >>> d = Divergence('RSI', 'Bullish', (1, 2), (3, 4), (5, 6), (7, 8), True)

        :param str indicator: The indicator for the divergence.
        :param str name: The name of the divergence.
        :param tuple x: The x points for the price.
        :param tuple y: The y points for the price.
        :param tuple ind_x: The x points for the indicator.
        :param tuple ind_y: The y points for the indicator.
        :param bool bullish: True if the divergence is bullish
        """
        self.indicator = indicator
        self.name = name
        self.x = x
        self.y = y
        self.ind_x = ind_x
        self.ind_y = ind_y
        self.bullish = bullish

    def to_dict(self):
        """
        Return a dictionary representation of the divergence.
        """
        return dict(
            indicator=self.indicator,
            name=self.name,
            bullish=self.bullish,
            x=self.x,
            y=self.y,
            ind_x=self.ind_x,
            ind_y=self.ind_y
        )

    def __repr__(self):
        args = [f'{k}={repr(v)}' for k, v in self.to_dict().items()]
        return f"{self.__class__.__name__}({', '.join(args)})"
