Harmonic Searches
-----------------
Harmonic searches are searches for ABC, ABCD or XABCD patterns.  On the final point of the pattern a price reversal is more likely to occur.  The MatrixSearch object performs this search using a very efficent algorithm.  A brute force 5 point search would constitute 

.. math:: complexity = O(n-m)^5

1000 candles with n = 100 peaks would consitiute a 100*99*98*97*96 search with 9034502400 passes!!

MatrixSearch is

.. math:: complexity = O(n^2/2 + (n-m)^2/2)

where

.. math:: n\2 <= m <= n


1000 candles with n = 100 peaks consitiutes a 100^2/2 ( lower triangle ) scan followed by an additional (n-m)^2/2 loops to link patterns. That's 5000 + 1250 passes to locate **all** patterns in the dataframe. That is 1445520 times faster than brute force.

.. note::
    It implies that instead of scanning one Asset in 30 seconds using a brute force approach you can now scan 1.446 Millions assets in the same 30 seconds.  The internet is now the slowest part of this problem.



.. code-block:: python
    :linenos:
    
    >>> from pyharmonics.marketdata import BinanceCandleData
    >>> from pyharmonics.search import HarmonicSearch
    >>> from pyharmonics.technicals import Technicals
    >>> b = BinanceCandleData()
    >>> b.get_candles('ETHUSDT', b.HOUR_4, 400)
    >>> t = Technicals(b.df, b.symbol, b.interval)
    >>> h = HarmonicSearch(t)
    >>> h.search()
    >>> patterns = h.get_patterns()
    >>> patterns[m.XABCD]
    []
    >>> patterns[m.ABCD]
    [ABCDPattern(name='ABCD-50-1.618', formed=True, retraces={'ABC': 0.5000347246336551, 'BCD': 3.31138888888889, 'ABCD': 3.31138888888889}, bullish=False, x=[Timestamp('2023-06-15 12:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-06-17 08:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-06-19 20:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-06-23 20:59:59+0100', tz='Europe/Dublin')], y=[1626.01, 1770.0, 1698.0, 1936.42], abc_extensions=[1936.42], completion_min_price=1930.992, completion_max_price=1930.992)]
    >>> patterns[m.ABCD][0]
    ABCDPattern(name='ABCD-50-1.618', formed=True, retraces={'ABC': 0.5000347246336551, 'BCD': 3.31138888888889, 'ABCD': 3.31138888888889}, bullish=False, x=[Timestamp('2023-06-15 12:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-06-17 08:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-06-19 20:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-06-23 20:59:59+0100', tz='Europe/Dublin')], y=[1626.01, 1770.0, 1698.0, 1936.42], abc_extensions=[1936.42], completion_min_price=1930.992, completion_max_price=1930.992)
    >>> patterns[m.ABC][0]
    ABCPattern(name=0.382, formed=True, retraces={'ABC': 0.386628628131977}, bullish=True, x=[Timestamp('2023-06-15 12:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-07-14 04:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-07-17 20:59:59+0100', tz='Europe/Dublin')], y=[1626.01, 2029.11, 1873.26], abc_extensions=[1873.26], completion_min_price=1873.26, completion_max_price=1873.26)
    >>> 

Here we can see a single ABCD pattern formed on ETHUSDT. Its completion time was ``Timestamp('2023-06-23 20:59:59+0100', tz='Europe/Dublin')``.  Data can be specifically referenced from the pattern object.

.. code-block:: python
    :linenos:
    
    >>> p = patterns[m.ABC][0]
    >>> p.name
    0.382
    >>> p.x
    [Timestamp('2023-06-15 12:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-07-14 04:59:59+0100', tz='Europe/Dublin'), Timestamp('2023-07-17 20:59:59+0100', tz='Europe/Dublin')]
    >>> p.y
    [1626.01, 2029.11, 1873.26]
    >>> 

As you can no doubt tell this information can be plotted with ``b.df`` to show you where the pattern is on the chart.