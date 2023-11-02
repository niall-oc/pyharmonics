__author__ = 'github.com/niall-oc'

import abc
from pyharmonics import constants
from hashlib import sha256

class HarmonicPattern(abc.ABC):
    @abc.abstractmethod
    def to_dict(self):
        raise NotImplementedError


class ABCPattern(HarmonicPattern):

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
        return f"ABCPattern({', '.join(args)})"

    def _set_hash(self):
        """
        A deterministic key for patterns.  This allows pattern generation to be idempotent
        """
        seed = f"{self.bullish}{self.name}{self.x[:-2]}{self.y[:-2]}{self.completion_min_price}{self.completion_max_price}"
        self.p_id = sha256(seed.encode()).hexdigest()

    def _set_CD_leg_extensions(self):
        C = self.y[-1]
        self.abc_extensions = [C]
        self.hop = C

    def _set_completion_price(self):
        C = self.y[-1]
        self.completion_min_price = C
        self.completion_max_price = C

class ABCDPattern(ABCPattern):
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
        return f"ABCDPattern({', '.join(args)})"

class XABCDPattern(ABCPattern):
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
        return f"XABCDPattern({', '.join(args)})"

class Divergence:
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
        self.indicator = indicator
        self.name = name
        self.x = x
        self.y = y
        self.ind_x = ind_x
        self.ind_y = ind_y
        self.bullish = bullish

    def to_dict(self):
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
        return f"Divergence({', '.join(args)})"
