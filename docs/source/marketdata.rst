Market data
-----------
pyharmonics requires pandas DataFrame objects.  You can create your own.  The schema required is shown below.  Pyharmonics can extract market data from Binance, Yahoo and Alpaca ( more to come ).

.. code-block:: python
    :linenos:

    >>> from pyharmonics.marketdata import YahooCandleData
    >>> y = YahooCandleData()
    >>> y.get_candles('MSFT', y.MIN_5, 300)
    >>> y.df
                                    open        high       close       close  volume
    index                                                                                                                  
    2023-07-06 18:15:00+01:00  342.410004  342.880005  342.858093  342.858093  299423
    2023-07-06 18:20:00+01:00  342.859985  342.989990  342.825012  342.825012  186800
    2023-07-06 18:25:00+01:00  342.829987  342.829987  342.029999  342.029999  253544
    2023-07-06 18:30:00+01:00  342.045013  342.109985  341.720001  341.720001  236668
    2023-07-06 18:35:00+01:00  341.779907  342.140015  342.089996  342.089996  190417
    ...                               ...         ...         ...         ...     ...
    2023-07-12 16:50:00+01:00  336.829987  336.869995  336.390015  336.390015  345811
    2023-07-12 16:55:00+01:00  336.369995  336.625000  336.429993  336.429993  301966
    2023-07-12 17:00:00+01:00  336.435486  337.154999  336.839996  336.839996  264732
    2023-07-12 17:05:00+01:00  336.829987  336.899994  336.684998  336.684998  200605
    2023-07-12 17:10:00+01:00  336.690002  337.229004  337.059998  337.059998  110316

    [300 rows x 5 columns]
    >>>

All candle data classes support MIN_1, MIN_5, MIN_15, HOUR_1, DAY_1, WEEK_1, MONTH_1, MONTH_3 time horizons.
BinanceCandleData and AplacaCandleData also support HOUR_2, HOUR_4, HOUR_8, MIN_3.
You can use any time frame you want.  You will need to supply this information later if you want to plot meaningfully.

CandleData that requires api keys.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python
    :linenos:

    >>> from pyharmonics.marketdata import AlpacaCandleData
    >>> key = dict('api'='whatever', 'secret'='whatever')
    >>> a = AlpacaCandleData(key)
    >>> a.get_candles('QQQ', y.MIN_5, 300)

Alpaca requires a dictionary with both a key and secret. Binance and Yahoo do not.  Binance can accept an API key if you have created one.  Order placement on any API requires a KEY but is not covered by this API.

.. warning::
    If you are supplying a key to **any API endpoint** please store those keys safely and never ever commit them accidentally to any repo.  Your keys are your account.  Losing control of them is losing control of your account.

Binance Usage:
~~~~~~~~~~~~~~

.. code-block:: python
    :linenos:

    >>> from pyharmonics.marketdata import BinanceCandleData
    >>> b = BinanceCandleData()
    >>> b.get_candles('ETHUSDT', b.MIN_5, 300)
    >>> b.df

                                  open     high      low    close     volume  close_time                       dts
    index                                                                                                         
    2023-09-12 10:04:59+01:00  1577.85  1578.82  1577.85  1578.07   778.5332  1694509499 2023-09-12 10:04:59+01:00
    2023-09-12 10:09:59+01:00  1578.07  1578.32  1577.16  1577.34   283.1288  1694509799 2023-09-12 10:09:59+01:00
    2023-09-12 10:14:59+01:00  1577.35  1578.15  1576.38  1577.90   525.5365  1694510099 2023-09-12 10:14:59+01:00
    2023-09-12 10:19:59+01:00  1577.91  1580.58  1577.90  1579.66   742.6356  1694510399 2023-09-12 10:19:59+01:00
    2023-09-12 10:24:59+01:00  1579.67  1580.28  1579.09  1579.42   622.7093  1694510699 2023-09-12 10:24:59+01:00
    ...                            ...      ...      ...      ...        ...         ...                       ...
    2023-09-13 10:39:59+01:00  1597.73  1600.48  1596.59  1599.01  1818.5411  1694597999 2023-09-13 10:39:59+01:00
    2023-09-13 10:44:59+01:00  1599.01  1600.91  1597.32  1598.05  1119.4597  1694598299 2023-09-13 10:44:59+01:00
    2023-09-13 10:49:59+01:00  1598.05  1598.35  1596.95  1597.11   499.6893  1694598599 2023-09-13 10:49:59+01:00
    2023-09-13 10:54:59+01:00  1597.12  1600.47  1597.11  1600.30   573.2835  1694598899 2023-09-13 10:54:59+01:00
    2023-09-13 10:59:59+01:00  1600.30  1602.44  1598.80  1600.20  2461.2631  1694599199 2023-09-13 10:59:59+01:00