pyharmonics
===========

pyharmonics detects harmonic patterns in OHLC candle data for any stock or crypto asset.  See http://www.harmonictrader.com for more information.



Market data usage
-----------------
.. code-block:: python
    :linenos:

    >>> from pyharmonics.marketdata import YahooCandleData
    >>> y = YahooCandleData()
    >>> y.get_candles('MSFT', y.MIN_5, 300)
    >>> y.df
                                    open        high       close       close  volume  close_time                       dts
    index                                                                                                                  
    2023-07-06 18:15:00+01:00  342.410004  342.880005  342.858093  342.858093  299423  1688663700 2023-07-06 18:15:00+01:00
    2023-07-06 18:20:00+01:00  342.859985  342.989990  342.825012  342.825012  186800  1688664000 2023-07-06 18:20:00+01:00
    2023-07-06 18:25:00+01:00  342.829987  342.829987  342.029999  342.029999  253544  1688664300 2023-07-06 18:25:00+01:00
    2023-07-06 18:30:00+01:00  342.045013  342.109985  341.720001  341.720001  236668  1688664600 2023-07-06 18:30:00+01:00
    2023-07-06 18:35:00+01:00  341.779907  342.140015  342.089996  342.089996  190417  1688664900 2023-07-06 18:35:00+01:00
    ...                               ...         ...         ...         ...     ...         ...                       ...
    2023-07-12 16:50:00+01:00  336.829987  336.869995  336.390015  336.390015  345811  1689177000 2023-07-12 16:50:00+01:00
    2023-07-12 16:55:00+01:00  336.369995  336.625000  336.429993  336.429993  301966  1689177300 2023-07-12 16:55:00+01:00
    2023-07-12 17:00:00+01:00  336.435486  337.154999  336.839996  336.839996  264732  1689177600 2023-07-12 17:00:00+01:00
    2023-07-12 17:05:00+01:00  336.829987  336.899994  336.684998  336.684998  200605  1689177900 2023-07-12 17:05:00+01:00
    2023-07-12 17:10:00+01:00  336.690002  337.229004  337.059998  337.059998  110316  1689178200 2023-07-12 17:10:00+01:00

    [300 rows x 7 columns]
    >>>

All candle data classes support MIN_1, MIN_5, MIN_15, HOUR_1, DAY_1, WEEK_1, MONTH_1, MONTH_3 time horizons.
BinanceCandleData and AplacaCandleData also support HOUR_2, HOUR_4, HOUR_8, MIN_3

CandleData that requires api keys.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python
    :linenos:

    >>> from pyharmonics.marketdata import AlpacaCandleData
    >>> key = dict('api'='whatever', 'secret'='whatever')
    >>> a = AlpacaCandleData(key)
    >>> a.get_candles('QQQ', y.MIN_5, 300)

Alpaca requires a dictionary with both a key and secret. Binance and Yahoo do not.  Binance can accep an API key if you have created one.  Order placement on any API requires a KEY but is not covered by this API.



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

As you can see the Techicals object adds more technical data to the dataframe.  This is the foundation for the harmonic object to discover and plot harmonic trading patterns.

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



Harmonic Searches
-----------------
Harmonic searches are searches for ABC, ABCD or XABCD patterns.  On the final point of the pattern a price reversal is more likely to occur.

.. code-block:: python
    :linenos:
    
    >>> from pyharmonics.marketdata import BinanceCandleData
    >>> from pyharmonics.search import MatrixSearch
    >>> from pyharmonics.technicals import Technicals
    >>> b = BinanceCandleData()
    >>> b.get_candles('ETHUSDT', b.HOUR_4, 400)
    >>> t = Technicals(b.df)
    >>> m = MatrixSearch(t)
    >>> m.search()
    >>> patterns = m.get_patterns()
    >>> patterns['XABCD']
    []
    >>> patterns['ABCD']
    [ABCDPattern(name='ABCD-50-1.618', formed=True, retraces={'ABC': 0.5000347246336551, 'BCD': 3.31138888888889, 'ABCD': 3.31138888888889}, bullish=False, x=[Timestamp('2023-06-15 12:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-06-17 08:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-06-19 20:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-06-23 20:59:59+0100', tz='Europe/Dublin')], y=[1626.01, 1770.0, 1698.0, 1936.42], abc_extensions=[1936.42], completion_min_price=1930.992, completion_max_price=1930.992)]
    >>> patterns['ABCD'][0]
    ABCDPattern(name='ABCD-50-1.618', formed=True, retraces={'ABC': 0.5000347246336551, 'BCD': 3.31138888888889, 'ABCD': 3.31138888888889}, bullish=False, x=[Timestamp('2023-06-15 12:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-06-17 08:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-06-19 20:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-06-23 20:59:59+0100', tz='Europe/Dublin')], y=[1626.01, 1770.0, 1698.0, 1936.42], abc_extensions=[1936.42], completion_min_price=1930.992, completion_max_price=1930.992)
    >>> patterns['ABC'][0]
    ABCPattern(name=0.382, formed=True, retraces={'ABC': 0.386628628131977}, bullish=True, x=[Timestamp('2023-06-15 12:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-07-14 04:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-07-17 20:59:59+0100', tz='Europe/Dublin')], y=[1626.01, 2029.11, 1873.26], abc_extensions=[1873.26], completion_min_price=1873.26, completion_max_price=1873.26)
    >>> 

Here we can see a single ABCD pattern formed on ETHUSDT. Its completion time was ``Timestamp('2023-06-23 20:59:59+0100', tz='Europe/Dublin')``.  Data can be specifically referenced from the pattern object.

.. code-block:: python
    :linenos:
    
    >>> p = patterns['ABC'][0]
    >>> p.name
    0.382
    >>> p.x
    [Timestamp('2023-06-15 12:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-07-14 04:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-07-17 20:59:59+0100', tz='Europe/Dublin')]
    >>> p.y
    [1626.01, 2029.11, 1873.26]
    >>> 

As you can no doubt tell this information can be plotted with ``b.df`` to show you where the pattern is on the chart. 