Using the Technicals object on OHLC Data
----------------------------------------
.. code-block:: python
    :linenos:

    >>> from pyharmonics.marketdata import BinanceCandleData
    >>> from pyharmonics.technicals import Technicals
    >>> b = BinanceCandleData()
    >>> t = Technicals(b.df, peak_spacing=20)
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/home/xual/Software/pyharmonics/src/pyharmonics/technicals.py", line 129, in __init__
        raise ValueError('Candle DataFrame is None! call cd.get_candles(ASSET, INTERVAL) first.')
    ValueError: Candle DataFrame is None! call cd.get_candles(ASSET, INTERVAL) first.

.. note::

    Always remember to get candle data :-)

.. code-block:: python
    :linenos:

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
    >>> t = Technicals(b.df)
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

As you can see the Techicals object adds more technical data to the dataframe.  This is the foundation for the harmonic object to discover and plot harmonic trading patterns. Tehcnicals object has an additional parameter called ``peak_spacing`` which determines the sensitivity to peaks.  Lower number is more sensitive.

.. code-block:: python
    :linenos:

    >>> t = Technicals(b.df, peak_spacing=12)

.. note::

    More peaks will mean more points to search through when looking for harmonic patterns.  In some cases this can lead to too many patterns being identified.

Technicals.df schema
~~~~~~~~~~~~~~~~~~~~
.. code-block:: python
    :linenos:
    
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
