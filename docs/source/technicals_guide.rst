Using the OHLCTechnicals object on OHLC Data
--------------------------------------------

.. code-block:: python

    >>> from pyharmonics.marketdata import BinanceCandleData
    >>> from pyharmonics.technicals import OHLCTechnicals
    >>> b = BinanceCandleData()
    >>> t = OHLCTechnicals(b.df, b.symbol, b.interval, peak_spacing=20)
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/xual/Software/pyharmonics/src/pyharmonics/technicals.py", line 129, in __init__
        raise ValueError('Candle DataFrame is None! call cd.get_candles(ASSET, INTERVAL) first.')
    ValueError: Candle DataFrame is None! call cd.get_candles(ASSET, INTERVAL) first.

.. note::

    Always remember to get candle data :-)

.. code-block:: python

    >>> b.get_candles('ETHUSDT', b.HOUR_4, 400)
    >>> b.df
                                open     high      low    close      volume  close_time                       dts
    index                                                                                                          
    2023-05-13 08:59:59+01:00  1805.62  1806.84  1796.80  1802.98  30365.3283  1683964799 2023-05-13 08:59:59+01:00
    2023-05-13 12:59:59+01:00  1802.98  1811.46  1801.24  1803.78  29164.0211  1683979199 2023-05-13 12:59:59+01:00
    2023-05-13 16:59:59+01:00  1803.79  1809.91  1785.23  1795.90  46713.5684  1683993599 2023-05-13 16:59:59+01:00
    2023-05-13 20:59:59+01:00  1795.91  1806.45  1786.12  1792.83  40715.0401  1684007999 2023-05-13 20:59:59+01:00
    2023-05-14 00:59:59+01:00  1792.84  1804.89  1792.38  1795.11  24692.1556  1684022399 2023-05-14 00:59:59+01:00
    ...                            ...      ...      ...      ...         ...         ...                       ...
    2023-07-18 04:59:59+01:00  1911.21  1917.19  1906.25  1908.88  19832.6141  1689652799 2023-07-18 04:59:59+01:00
    2023-07-18 08:59:59+01:00  1908.88  1911.72  1893.36  1898.99  37921.2814  1689667199 2023-07-18 08:59:59+01:00
    2023-07-18 12:59:59+01:00  1898.99  1909.64  1890.80  1894.15  39215.5098  1689681599 2023-07-18 12:59:59+01:00
    2023-07-18 16:59:59+01:00  1894.15  1903.66  1885.08  1897.20  49833.1236  1689695999 2023-07-18 16:59:59+01:00
    2023-07-18 20:59:59+01:00  1897.21  1903.58  1875.73  1891.50  46447.8182  1689710399 2023-07-18 20:59:59+01:00

    [400 rows x 7 columns]
    >>> t = Technicals(b.df, b.symbol, b.interval)
    >>> t.df
                                open     high      low    close      volume  close_time  ... price_peaks  price_dips  macd_peaks  macd_dips  rsi_peaks  rsi_dips
    index                                                                                  ...                                                                    
    2023-05-13 08:59:59+01:00  1805.62  1806.84  1796.80  1802.98  30365.3283  1683964799  ...           0           0           0          0          0         0
    2023-05-13 12:59:59+01:00  1802.98  1811.46  1801.24  1803.78  29164.0211  1683979199  ...           0           0           0          0          0         0
    2023-05-13 16:59:59+01:00  1803.79  1809.91  1785.23  1795.90  46713.5684  1683993599  ...           0           0           0          0          0         0
    2023-05-13 20:59:59+01:00  1795.91  1806.45  1786.12  1792.83  40715.0401  1684007999  ...           0           0           0          0          0         0
    2023-05-14 00:59:59+01:00  1792.84  1804.89  1792.38  1795.11  24692.1556  1684022399  ...           0           0           0          0          0         0
    ...                            ...      ...      ...      ...         ...         ...  ...         ...         ...         ...        ...        ...       ...
    2023-07-18 04:59:59+01:00  1911.21  1917.19  1906.25  1908.88  19832.6141  1689652799  ...           0           0           0          0          0         0
    2023-07-18 08:59:59+01:00  1908.88  1911.72  1893.36  1898.99  37921.2814  1689667199  ...           0           0           0          0          0         0
    2023-07-18 12:59:59+01:00  1898.99  1909.64  1890.80  1894.15  39215.5098  1689681599  ...           0           0           0          0          0         0
    2023-07-18 16:59:59+01:00  1894.15  1903.66  1885.08  1897.20  49833.1236  1689695999  ...           0           0           0          0          0         0
    2023-07-18 20:59:59+01:00  1897.21  1903.58  1875.73  1891.50  46447.8182  1689710399  ...           0           0           0          0          0         0

    [400 rows x 27 columns]


Peak sensitivity can be increased like so.

.. code-block:: python

    >>> t = Technicals(b.df, peak_spacing=12)

.. note::

    More peaks will mean more points to search through when looking for harmonic patterns.  In some cases this can lead to too many patterns being identified.


Using the standard Technicals object on single trend data
---------------------------------------------------------
.. code-block:: python

    >>> from pyharmonics.technicals import Technicals
    >>> from pyharmonics.utils import UER
    >>> t = Technicals(UER, 'Unemployment', 'monthly', peak_spacing=6)
    >>> t.df
            year  close  price_peaks  price_dips      macd        rsi  stoch_rsi  ...    ema 21    ema 34    ema 55  macd_peaks  macd_dips  rsi_peaks  rsi_dips
    0    2013-01-01    8.0            1           0       NaN        NaN        NaN  ...       NaN       NaN       NaN           0          0          0         0
    1    2013-02-01    7.7            0           0       NaN        NaN        NaN  ...       NaN       NaN       NaN           0          0          0         0
    2    2013-03-01    7.5            0           0       NaN        NaN        NaN  ...       NaN       NaN       NaN           0          0          0         0
    3    2013-04-01    7.6            0           0       NaN        NaN        NaN  ...       NaN       NaN       NaN           0          0          0         0
    4    2013-05-01    7.5            0           0       NaN        NaN        NaN  ...       NaN       NaN       NaN           0          0          0         0
    ..          ...    ...          ...         ...       ...        ...        ...  ...       ...       ...       ...         ...        ...        ...       ...
    122  2023-03-01    3.5            0           0  0.036866  38.289828   0.591382  ...  4.069905  4.441627  4.740887           0          0          0         0
    123  2023-04-01    3.4            0           1  0.042426  37.160633   0.686581  ...  4.009005  4.382106  4.692998           0          0          0         0
    124  2023-05-01    3.7            1           0  0.068006  42.627002   0.736196  ...  3.980914  4.343128  4.657534           0          0          1         0
    125  2023-06-01    3.6            0           0  0.079110  41.336196   0.769141  ...  3.946285  4.300664  4.619765           0          0          0         0
    126  2023-07-01    3.5            0           0  0.080380  40.030762   0.794174  ...  3.905714  4.254912  4.579774           1          0          0         0

    [127 rows x 22 columns]


Technicals.df schema
~~~~~~~~~~~~~~~~~~~~
.. code-block:: python
    
    >>> t.df.columns
    Index(['open', 'high', 'low', 'close', 'volume', 'close_time', 'dts', 'macd',
        'rsi', 'stoch_rsi', 'bb%', 'sma 50', 'sma 100', 'sma 150', 'sma 200',
        'ema 5', 'ema 8', 'ema_13', 'ema 21', 'ema 34', 'ema 55', 'price_peaks',
        'price_dips', 'macd_peaks', 'macd_dips', 'rsi_peaks', 'rsi_dips'],
        dtype='object')


* ```'macd', 'rsi', 'stoch_rsi', 'bb%'``` are the MACD ( Moving Avg. Convergence Divergence ), RSI ( Relative strength index ), Stochastic RSI and Bollinger Band deviation reading.
* ```'sma 50', 'sma 100', 'sma 150', 'sma 200'``` are Simple Moving Avergaes SMA.  50, 100, 150, 200 candle average.  All useful for plotting support/resistance levels.
* ```'ema 5', 'ema 8', 'ema_13', 'ema 21', 'ema 34', 'ema 55'``` are Exponential moving averages all fibonacci numbers.  Very accurate in plotting support/resistance as swings move.
* ```'price_peaks', 'price_dips', 'macd_peaks', 'macd_dips', 'rsi_peaks', 'rsi_dips'``` the indexes where the price is at a peak or dip.  Similar for the MACD and RSI.  This informatoin is key for detecting divergence patterns which confirm harmonic patterns.