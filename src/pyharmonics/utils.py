__author__ = 'github.com/niall-oc'

from pyharmonics import constants
from copy import deepcopy
import numpy as np
import pandas as pd
from io import StringIO

UER = pd.read_csv(
    StringIO(
        'year,close\n2013-01-01,8.0\n2013-02-01,7.7\n2013-03-01,7.5\n2013-04-01,7.6\n2013-05-01,7.5\n'
        '2013-06-01,7.5\n2013-07-01,7.3\n2013-08-01,7.2\n2013-09-01,7.2\n2013-10-01,7.2\n2013-11-01,6.9\n'
        '2013-12-01,6.7\n2014-01-01,6.6\n2014-02-01,6.7\n2014-03-01,6.7\n2014-04-01,6.2\n2014-05-01,6.3\n'
        '2014-06-01,6.1\n2014-07-01,6.2\n2014-08-01,6.1\n2014-09-01,5.9\n2014-10-01,5.7\n2014-11-01,5.8\n'
        '2014-12-01,5.6\n2015-01-01,5.7\n2015-02-01,5.5\n2015-03-01,5.4\n2015-04-01,5.4\n2015-05-01,5.6\n'
        '2015-06-01,5.3\n2015-07-01,5.2\n2015-08-01,5.1\n2015-09-01,5.0\n2015-10-01,5.0\n2015-11-01,5.1\n'
        '2015-12-01,5.0\n2016-01-01,4.8\n2016-02-01,4.9\n2016-03-01,5.0\n2016-04-01,5.1\n2016-05-01,4.8\n'
        '2016-06-01,4.9\n2016-07-01,4.8\n2016-08-01,4.9\n2016-09-01,5.0\n2016-10-01,4.9\n2016-11-01,4.7\n'
        '2016-12-01,4.7\n2017-01-01,4.7\n2017-02-01,4.6\n2017-03-01,4.4\n2017-04-01,4.4\n2017-05-01,4.4\n'
        '2017-06-01,4.3\n2017-07-01,4.3\n2017-08-01,4.4\n2017-09-01,4.3\n2017-10-01,4.2\n2017-11-01,4.2\n'
        '2017-12-01,4.1\n2018-01-01,4.0\n2018-02-01,4.1\n2018-03-01,4.0\n2018-04-01,4.0\n2018-05-01,3.8\n'
        '2018-06-01,4.0\n2018-07-01,3.8\n2018-08-01,3.8\n2018-09-01,3.7\n2018-10-01,3.8\n2018-11-01,3.8\n'
        '2018-12-01,3.9\n2019-01-01,4.0\n2019-02-01,3.8\n2019-03-01,3.8\n2019-04-01,3.6\n2019-05-01,3.7\n'
        '2019-06-01,3.6\n2019-07-01,3.7\n2019-08-01,3.7\n2019-09-01,3.5\n2019-10-01,3.6\n2019-11-01,3.6\n'
        '2019-12-01,3.6\n2020-01-01,3.5\n2020-02-01,3.5\n2020-03-01,4.4\n2020-04-01,14.7\n2020-05-01,13.2\n'
        '2020-06-01,11.0\n2020-07-01,10.2\n2020-08-01,8.4\n2020-09-01,7.9\n2020-10-01,6.9\n2020-11-01,6.7\n'
        '2020-12-01,6.7\n2021-01-01,6.3\n2021-02-01,6.2\n2021-03-01,6.1\n2021-04-01,6.1\n2021-05-01,5.8\n'
        '2021-06-01,5.9\n2021-07-01,5.4\n2021-08-01,5.2\n2021-09-01,4.8\n2021-10-01,4.5\n2021-11-01,4.2\n'
        '2021-12-01,3.9\n2022-01-01,4.0\n2022-02-01,3.8\n2022-03-01,3.6\n2022-04-01,3.6\n2022-05-01,3.6\n'
        '2022-06-01,3.6\n2022-07-01,3.5\n2022-08-01,3.7\n2022-09-01,3.5\n2022-10-01,3.7\n2022-11-01,3.6\n'
        '2022-12-01,3.5\n2023-01-01,3.4\n2023-02-01,3.6\n2023-03-01,3.5\n2023-04-01,3.4\n2023-05-01,3.7\n'
        '2023-06-01,3.6\n2023-07-01,3.5\n'
    )
)


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

def find_peaks(data, comparator, axis=0, order=1, mode='clip'):
    """
    Calculate the relative extrema of `data`.
    Relative extrema are calculated by finding locations where
    ``comparator(data[n], data[n+1:n+order+1])`` is True.
    Parameters
    ----------
    data : ndarray
        Array in which to find the relative extrema.
    comparator : callable
        Function to use to compare two data points.
        Should take two arrays as arguments.
    axis : int, optional
        Axis over which to select from `data`. Default is 0.
    order : int, optional
        How many points on each side to use for the comparison
        to consider ``comparator(n,n+x)`` to be True.
    mode : str, optional
        How the edges of the vector are treated. 'wrap' (wrap around) or
        'clip' (treat overflow as the same as the last (or first) element).
        Default 'clip'. See numpy.take.
    Returns
    -------
    extrema : ndarray
        Boolean array of the same shape as `data` that is True at an extrema,
        False otherwise.
    See also
    --------
    argrelmax, argrelmin
    Examples
    --------
    >>> import numpy as np
    >>> testdata = np.array([1,2,3,2,1])
    >>> self.find_peaks(testdata, np.greater, axis=0)
    array([False, False,  True, False, False], dtype=bool)
    """
    if (int(order) != order) or (order < 1):
        raise ValueError('Order must be an int >= 1')

    datalen = data.shape[axis]
    locs = np.arange(0, datalen)

    results = np.ones(data.shape, dtype=bool)
    main = data.take(locs, axis=axis, mode=mode)
    for shift in range(1, order + 1):
        plus = data.take(locs + shift, axis=axis, mode=mode)
        minus = data.take(locs - shift, axis=axis, mode=mode)
        results &= comparator(main, plus)
        results &= comparator(main, minus)
        if ~results.any():
            break
    # Calculate plateaus
    plateaus = (data == np.roll(data, 1))
    for i in range(len(plateaus)):
        # Just passed a plateau
        if plateaus[i]:
            # Remove the first registered peak in a plateau leaving the latter only as a peak
            results[i - 1] = False
    return results
