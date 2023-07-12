# pyharmonics

pyharmonics detects harmonic patterns in OHLC candle data for any stock or crypto asset.  See http://www.harmonictrader.com for more information.

## Market data usage
```
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
```
All candle data classes support MIN_1, MIN_5, MIN_15, HOUR_1, DAY_1, WEEK_1, MONTH_1, MONTH_3 time horizons.
BinanceCandleData and AplacaCandleData also support HOUR_2, HOUR_4, HOUR_8, MIN_3

## CandleData that requires api keys.
```
>>> from pyharmonics.marketdata import AlpacaCandleData
>>> key = dict('api'='whatever', 'secret'='whatever')
>>> a = AlpacaCandleData(key)
```
Alpaca requires a dictionary with both a key and secret. Binance and Yahoo do not.  Binance can accep an API key if you have created one.  Order placement on any API requires a KEY but is not covered by this API.
