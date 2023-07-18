__author__ = 'github.com/niall-oc'

from pyharmonics import constants
from copy import deepcopy


def get_pattern_retraces(prices: list) -> dict:
    """
    Parameters
    ----------
    classification: string
        Defined in trigger.constants can be 'XABCD', 'ABCD', 'ABC'
    prices : list
        Prices of pattern.
    ----------
    returns dict
    """
    points = len(prices)
    if points == 3:  # ABC
        retraces = {
            constants.ABC: abs(prices[0] - prices[1]) / abs(prices[2] - prices[1])
        }
    elif points == 4:  # ABCD
        retraces = {
            constants.ABC: abs(prices[0] - prices[1]) / abs(prices[2] - prices[1]),
            constants.BCD: abs(prices[1] - prices[2]) / abs(prices[2] - prices[3]),
            constants.ABCD: abs(prices[1] - prices[2]) / abs(prices[2] - prices[3])
        }
    elif points == 5:  # XABCD
        retraces = {
            constants.XAB: abs(prices[0] - prices[1]) / abs(prices[2] - prices[1]),
            constants.ABC: abs(prices[1] - prices[2]) / abs(prices[2] - prices[3]),
            constants.BCD: abs(prices[2] - prices[3]) / abs(prices[3] - prices[4])
        }
        if prices[1] > prices[2]:  # point A is above point B
            if prices[1] > prices[3]:
                # Crab, Gartley, Bat, Butterfly patterns.
                retraces[constants.XABCD] = abs(prices[0] - prices[1]) / abs(prices[4] - prices[1])
            else:
                # Cypher and Shark patterns.
                retraces[constants.XABCD] = abs(prices[0] - prices[3]) / abs(prices[4] - prices[3])
        else:  # bearish
            if prices[1] < prices[3]:
                # Crab, Gartley, Bat, Butterfly patterns.
                retraces[constants.XABCD] = abs(prices[0] - prices[1]) / abs(prices[4] - prices[1])
            else:
                # Cypher and Shark patterns.
                retraces[constants.XABCD] = abs(prices[0] - prices[3]) / abs(prices[4] - prices[3])
    else:
        raise ValueError(f'{prices} must be of len 3, 4, 5 for ABC, ABCD, XABCD pattern retraces respectively')
    return retraces


def get_pattern_direction(prices: list) -> str:
    """
    All patterns forming a final retrace where the price is moving down are
    indicating a reversal to the upside is iminent.  This is bullish.

    The opposite final retrace where the price is moving up is bearish.
    Parameters
    ----------
    prices : list
        Prices of pattern.
    ----------
    returns str
    """
    if prices[-1] < prices[-2]:
        return constants.BULLISH
    else:
        return constants.BEARISH


def is_pattern_formed(name: str, retrace: float, patterns: dict) -> bool:
    """
    Do the pattern retraces reach the required levels to be deemed formed?

    Parameters
    ----------
    retraces: dict
        key is defined in trigger.constants, value is the retrace value for that retrace.  This was already
        calculated in the search object and is safe to pass to the Events object.
    ----------
    returns bool
    """
    if name in constants.ABCDS:
        return retrace >= patterns[constants.ABCD][name][constants.MIN]
    elif name in constants.XABCDS:
        return retrace >= patterns[constants.XABCD][name][constants.MIN]
    else:
        raise KeyError(f"{name} not in {constants.ABCDS} or {constants.XABCDS}")
    return False


def get_pattern_definition(tolerance: float, patterns: dict) -> dict:
    """
    Harmonic pattern definitions must have their min and max thresholds widened by a percentage

    Parameters
    ----------
    tolerance: float
        0.03 is 3 percent tolerance
    ----------
    returns copy of adjusted patterns
    """
    harmonic_patterns = deepcopy(patterns)
    # set pattern fib_tolerance
    for stage, patterns in harmonic_patterns.items():
        for pattern, details in patterns.items():
            details[constants.MIN] = details[constants.MIN] * (1 - tolerance)
            details[constants.MAX] = details[constants.MAX] * (1 + tolerance)
    return harmonic_patterns


def get_candle_span(candle_time, candle_gap: int, num_gaps: int) -> list:
    """
    Generates a list of time indexes that span a specific time.
    Useful for finding peaks on indicators that are near peaks on oscilators

    >>> utils.get_candle_span(10, 1, 3)
    [7, 8, 9, 10, 11, 12, 13]
    >>> utils.get_candle_span(100, 10, 3)
    [70, 80, 90, 100, 110, 120, 130]
    """
    return list(range(candle_time - (candle_gap * num_gaps), candle_time + (candle_gap * num_gaps) + candle_gap, candle_gap))


def match_peaks(indicator_peaks: list, price_peaks: list, index_span: int) -> list:
    """

    >>> indicator_peaks = [45, 62, 99, 134, 157, 176, 211, 243, 258, 296, 311, 333, 348, 391, 422, 447, 474,
                            524, 540, 581, 617, 635, 647, 664, 719, 737, 766, 786, 817, 862, 910, 932, 970, 998]
    >>> price_peaks = [0, 20, 45, 49, 74, 89, 98, 112, 121, 134, 145, 156, 183, 197, 216, 233, 243, 255, 258,
                        278, 296, 301, 310, 314, 359, 377, 391, 423, 427, 456, 470, 478, 507, 519, 521, 537, 543,
                        553, 567, 580, 600, 611, 626, 635, 647, 648, 664, 681, 694, 712, 723, 737, 743, 759, 766,
                        784, 789, 807, 817, 833, 853, 862, 881, 927, 949, 970, 989, 997, 999]
    >>> utils.match_peaks(indicator_peaks, price_peaks, 3)
    [(45, 45), (99, 98), (134, 134), (157, 156), (243, 243), (258, 258), (296, 296), (311, 310), (391, 391), (422, 423),
     (581, 580), (635, 635), (647, 647), (664, 664), (737, 737), (766, 766), (786, 784), (817, 817), (862, 862), (970, 970), (998, 997)]
    """
    # Setup while loop indexes and limits
    matches = []
    max_indicator, max_price = len(indicator_peaks), len(price_peaks)
    ind_i = pri_i = 0
    while ind_i < max_indicator and pri_i < max_price:
        # if the price index is between the (indicator index - an offset) and (indicator index + an offset)
        if price_peaks[pri_i] > indicator_peaks[ind_i] - index_span and price_peaks[pri_i] < indicator_peaks[ind_i] + index_span:
            matches.append((indicator_peaks[ind_i], price_peaks[pri_i],))
            ind_i += 1
        elif price_peaks[pri_i] > indicator_peaks[ind_i] + index_span:
            ind_i += 1
        else:
            pri_i += 1
    return matches


def set_completion_price(pattern):
    """
    Given a pattern, calculate the completion price range
    """
    X = pattern.y[0]
    A = pattern.y[1]
    C = pattern.y[3]
    peak_price = C if C > A else A
    completion_retraces = constants.MATRIX_PATTERNS[pattern.classification][pattern.name]
    if pattern.bullish:
        completion_min_price = peak_price - ((peak_price - X) * completion_retraces[constants.MIN])
        completion_max_price = peak_price - ((peak_price - X) * completion_retraces[constants.MAX])

    else:
        completion_min_price = peak_price + ((X - peak_price) * completion_retraces[constants.MIN])
        completion_max_price = peak_price + ((X - peak_price) * completion_retraces[constants.MAX])
    return completion_min_price, completion_max_price


def set_CD_leg_extensions(pattern):
    """

    """
    A = pattern.y[-4]
    B = pattern.y[-3]
    C = pattern.y[-2]
    move = abs(A - B)

    ext = [e for e in sorted(constants.EXTENSIONS)]
    if pattern.bullish:
        abc_extensions = [C - (e * move) for e in ext]
        # self.hop = self.abc_extensions[-1]
        for e in abc_extensions:
            if e < pattern.completion_max_price:
                pattern.hop = e
                break
    else:
        abc_extensions = [C + (e * move) for e in ext]
        # self.hop = self.abc_extensions[-1]
        for e in abc_extensions:
            if e > pattern.completion_max_price:
                hop = e
                break
    return abc_extensions, hop


def line_slope(y2: float, y1: float, x2: int, x1: int) -> float:
    y_diff = y2 - y1
    if bool(y_diff):
        return y_diff / (x2 - x1)
    else:
        return 0
