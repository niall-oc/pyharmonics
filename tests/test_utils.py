from pyharmonics import utils
from pyharmonics import constants
import pytest


def test_get_pattern_retraces_xabcd():
    prices = [2, 10, 6, 8, 3]
    retraces = utils.get_pattern_retraces(prices)
    assert (constants.XAB in retraces.keys())
    assert (constants.ABC in retraces.keys())
    assert (constants.BCD in retraces.keys())
    assert (constants.XABCD in retraces.keys())


def test_get_pattern_retraces_abcd():
    prices = [10, 6, 8, 3]
    retraces = utils.get_pattern_retraces(prices)
    assert (constants.ABC in retraces.keys())
    assert (constants.ABCD in retraces.keys())
    assert (constants.XABCD not in retraces.keys())
    assert (constants.XAB not in retraces.keys())


def test_get_pattern_retraces_abc():
    prices = [10, 6, 8]
    retraces = utils.get_pattern_retraces(prices)
    assert (constants.ABC in retraces.keys())
    assert (constants.BCD not in retraces.keys())
    assert (constants.ABCD not in retraces.keys())
    assert (constants.XABCD not in retraces.keys())
    assert (constants.XAB not in retraces.keys())


def test_get_pattern_retraces_raises():
    prices = [10, 6]
    with pytest.raises(ValueError):
        utils.get_pattern_retraces(prices)

    prices = [10, 6, 4, 5, 6, 7, 8]
    with pytest.raises(ValueError):
        utils.get_pattern_retraces(prices)


def test_get_pattern_direction():
    prices = [1, 2]
    assert (constants.BEARISH == utils.get_pattern_direction(prices))
    prices = [2, 1]
    assert (constants.BULLISH == utils.get_pattern_direction(prices))


def test_is_pattern_formed():
    patterns = utils.get_pattern_definition(0.03, constants.MATRIX_PATTERNS)
    assert (utils.is_pattern_formed(constants.BAT, 0.886, patterns))
    assert (not utils.is_pattern_formed(constants.BAT, 0.676, patterns))
    with pytest.raises(KeyError):
        assert (utils.is_pattern_formed('fake-pattern', 0.886, patterns))


def test_get_pattern_definition():
    patterns = utils.get_pattern_definition(0.03, constants.MATRIX_PATTERNS)
    assert (0.85942 == patterns[constants.XABCD][constants.BAT][constants.MIN])
    assert (0.9125800000000001 == patterns[constants.XABCD][constants.BAT][constants.MAX])


def test_get_candle_span():
    span = utils.get_candle_span(10, 1, 3)
    assert (span == [7, 8, 9, 10, 11, 12, 13])
    span = utils.get_candle_span(100, 10, 3)
    assert (span == [70, 80, 90, 100, 110, 120, 130])


def test_match_peaks():
    indicator_peaks = [45, 62, 99, 134, 157, 176, 211, 243, 258, 296, 311, 333, 348, 391, 422, 447, 474,
                       524, 540, 581, 617, 635, 647, 664, 719, 737, 766, 786, 817, 862, 910, 932, 970, 998]
    price_peaks = [0, 20, 45, 49, 74, 89, 98, 112, 121, 134, 145, 156, 183, 197, 216, 233, 243, 255, 258,
                   278, 296, 301, 310, 314, 359, 377, 391, 423, 427, 456, 470, 478, 507, 519, 521, 537, 543,
                   553, 567, 580, 600, 611, 626, 635, 647, 648, 664, 681, 694, 712, 723, 737, 743, 759, 766,
                   784, 789, 807, 817, 833, 853, 862, 881, 927, 949, 970, 989, 997, 999]
    matches = utils.match_peaks(indicator_peaks, price_peaks, 3)
    results = [(45, 45), (99, 98), (134, 134), (157, 156), (243, 243), (258, 258), (296, 296), (311, 310), (391, 391), (422, 423),
               (581, 580), (635, 635), (647, 647), (664, 664), (737, 737), (766, 766), (786, 784), (817, 817), (862, 862), (970, 970), (998, 997)]
    assert (matches == results)


def test_line_slope():
    assert utils.line_slope(5, 2, 6, 3) == 1
    assert utils.line_slope(3, 3, 5, 2) == 0
    assert utils.line_slope(2, 6, 1, 4) == 1.3333333333333333
