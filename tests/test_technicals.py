__author__ = 'github.com/niall-oc'

from pyharmonics.marketdata import BinanceCandleData
from pyharmonics.technicals import OHLCTechnicals, SingleTechnicals
import pandas as pd
import numpy as np

b = BinanceCandleData()
b._set_params('BTCUSDT', b.HOUR_1, 1000, None, None)
b.df = pd.read_pickle('tests/data/btc_test_data')
t = OHLCTechnicals(b.df, b.symbol, b.interval, peak_spacing=20)

def test_price_dips():
    given = t.get_peak_x_y(t.PRICE_DIPS)
    expected = (
        np.array([20, 49, 89, 121, 145, 197, 233, 278, 314, 377, 427, 456, 521, 567, 626, 723, 759, 807, 833, 927, 989]),
        np.array([18711.87, 18125.98, 18531.42, 18805.34, 18629.2, 18471.28, 18843.01, 19159.42, 18920.35, 19730.0, 19320.0,
                  19237.14, 18860.0, 18190.0, 18975.18, 18900.0, 18650.0, 19070.11, 19157.0, 20000.09, 20427.23])
    )
    assert np.all(np.equal(given, expected))

def test_price_peaks():
    given = t.get_peak_x_y(t.PRICE_PEAKS)
    expected = (
        np.array([0, 45, 74, 183, 216, 258, 359, 391, 470, 580, 681, 737, 784, 786, 817, 881, 949, 997]),
        np.array([19686.2, 19956.0, 19550.17, 20385.86, 19790.0, 20185.0, 20475.0, 20456.6, 19558.0, 19951.87, 19706.66,
                  19347.82, 19257.0, 19257.0, 19695.0, 21020.0, 21085.0, 20845.92])
    )

def test_macd_dips():
    given = t.get_peak_x_y(t.MACD_DIPS)
    expected = (
        np.array([89, 122, 145, 190, 232, 265, 305, 377, 428, 457, 493, 569, 598, 694, 745, 826, 901, 965]),
        np.array([-81.45159225085027, -23.38146352024897, -24.86275005397194, -169.05928488782354, -48.265404977943874,
                  -32.58365842521273, -14.464184383740182, -57.67453791350911, -50.85238451795732, -3.5243323551074965,
                  -20.367551607571414, -76.73096552830059, -79.63032531195469, -46.21268329563041, -12.302400786728025,
                  -24.96498132310041, -52.10299789998075, -22.112003457981658])
    )
    assert np.all(np.equal(given, expected))

def test_macd_peaks():
    given = t.get_peak_x_y(t.MACD_PEAKS)
    expected = (
        np.array([99, 134, 176, 211, 258, 296, 333, 391, 447, 474, 524, 581, 664, 737, 766, 817, 862, 932, 998]),
        np.array([51.25290156987122, 11.780399148583387, 111.15482317217374, 104.01744114300635, 29.81425985268349,
                  10.706606334658176, 45.645235880899705, 22.68622587687249, 18.76306582254196, 20.938535838566775,
                  18.43976419513654, 91.21293968047434, 33.52283116056065, 23.10009211217998, 25.349945765522317,
                  41.47756433642398, 107.36348497277888, 61.22262762669066, 25.555579759624614])
    )
    assert np.all(np.equal(given, expected))

def test_rsi_dips():
    given = t.get_peak_x_y(t.RSI_DIPS)
    expected = (
        np.array([51, 88, 121, 144, 197, 232, 301, 377, 427, 456, 491, 567, 625, 694, 723, 759, 807, 852, 922, 989]),
        np.array([34.25323100483362, 32.09885326243845, 39.51078170520284, 33.03075415580916, 27.691911224650852,
                  36.37757252402807, 28.275696801956457, 39.048210677256556, 24.940397796151274, 28.891818261423694,
                  30.647302337476802, 15.496534342661008, 35.46996606108307, 33.112056808682894, 30.72529835327377,
                  31.378665327023626, 44.149980605814314, 39.58299092418385, 30.854104865166292, 36.139944627070506])
    )
    assert np.all(np.equal(given, expected))

def test_rsi_peaks():
    given = t.get_peak_x_y(t.RSI_PEAKS)
    expected = (
        np.array([44, 74, 97, 134, 174, 216, 257, 359, 422, 474, 580, 646, 737, 785, 817, 861, 948, 997]),
        np.array([74.76472535906501, 61.3615885512112, 62.292386517952714, 55.70451725634307, 79.26150656630413,
                  62.44746505939419, 66.8770900501026, 76.03742036689171, 48.70750965396278, 58.30001351597064,
                  74.04533875608922, 74.82638896793428, 60.6564712900872, 63.42521741490593, 81.45732011464193,
                  90.41181403153934, 71.63007067733558, 57.871009640915])
    )
    assert np.all(np.equal(given, expected))

def test_single_trend_technicals():
    of = pd.DataFrame(b.df[['close']])
    st = SingleTechnicals(of)
    assert len(of) > 0
    assert SingleTechnicals.PRICE_PEAKS in list(t.df.columns)

if __name__ == '__main__':
    # For debugging
    test_rsi_dips()
