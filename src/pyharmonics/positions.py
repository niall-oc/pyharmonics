__author__ = 'github.com/niall-oc'

from pyharmonics import constants
from hashlib import sha256
import datetime

class Position:
    def __init__(self, pattern, strike, dollar_amount):
        """
        Represents a position for a trade.

        :param pyharmonics.pattern.HarmonicPattern pattern: A subclass of HarmonicPattern representing a set of price levels.
        :param float strike: The price at which the position was entered.
        :param float dollar_amount: The size of the position in dollars.
        """
        self.symbol = pattern.symbol
        self.pattern = pattern
        self.long = self.pattern.bullish
        self.strike = strike
        self.dollar_amount = dollar_amount
        self.timestamp = datetime.datetime.now()
        self.status = constants.WAITING
        self.target_hit = constants.WAITING
        self._set_targets(pattern.y[-2])
        self._set_stop()
        self._set_stats()

    def _set_stop(self):
        """
        The stop price is the smaller between the Strike - hop, or 1/3 of the strike - t1
        """
        limit = abs(self.targets[0] - self.strike) / 3
        if self.long:
            self.stop = self.strike - limit
        else:
            self.stop = self.strike + limit

    def _set_targets(self, C):
        """
        """
        t1_amount = abs(C - self.strike) / 2
        t3_amount = abs(C - self.strike) * constants.E_1618

        if self.long:
            self.targets = [self.strike + t1_amount, C, self.strike + t3_amount]
        else:
            self.targets = [self.strike - t1_amount, C, self.strike - t3_amount]

    def _set_stats(self):
        """
        Calculate loss and gains for all outcomes.
        """
        position_amount = self.dollar_amount / len(self.targets)

        # Set the percentage moves for this patten/position
        self.moves = {
            'stop': min(self.stop, self.strike) / max(self.stop, self.strike)
        }
        self.outcomes = {
            'stop': position_amount * self.moves['stop']
        }
        for n, t in enumerate(self.targets, 1):
            key = f"t{n}"
            self.moves[key] = max(t, self.strike) / min(t, self.strike)
            # Inverse percentages for shorts
            if not self.long:
                self.moves[key] = abs((1 / self.moves[key]) - 1) + 1
            self.outcomes[key] = position_amount * self.moves[key]
        self.outcomes['position_size'] = position_amount
        if self.target_hit == constants.STOPPED:
            self.percent = (self.outcomes['stop'] * 3) / self.dollar_amount
        elif self.target_hit == constants.TARGET1:
            self.percent = (self.outcomes['t1'] + self.outcomes['stop'] + self.outcomes['stop']) / self.dollar_amount
        elif self.target_hit == constants.TARGET2:
            self.percent = (self.outcomes['t1'] + self.outcomes['t2'] + self.outcomes['stop']) / self.dollar_amount
        elif self.target_hit == constants.TARGET3:
            self.percent = (self.outcomes['t1'] + self.outcomes['t2'] + self.outcomes['t3']) / self.dollar_amount

    def to_dict(self):
        return dict(
            symbol=self.symbol,
            pattern=self.pattern,
            long=self.long,
            strike=self.strike,
            dollar_amount=self.dollar_amount,
            targets=self.targets,
            stop=self.stop,
            timestamp=self.timestamp,
            status=self.status,
            outcomes=self.outcomes,
            moves=self.moves,
            percent=self.percent,
            target_hit=self.target_hit
        )

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        args = [f'{k}={repr(v)}' for k, v in self.to_dict().items()]
        return f"{self._cls }({', '.join(args)})"
