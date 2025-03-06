Quick functions
===============

.. code-block:: python

    >>> from pyharmonics.quick import *

This gives you.

.. code-block:: python

    from pyharmonics.marketdata import YahooCandleData, BinanceCandleData, YahooOptionData
    from pyharmonics.technicals import OHLCTechnicals, Technicals
    from pyharmonics.search import HarmonicSearch, DivergenceSearch
    from pyharmonics.positions import Position
    from pyharmonics.plotter import HarmonicPlotter, PositionPlotter, OptionPlotter
    from pyharmonics import constants

You also get some quick functions for plot/displaying the current status of a asset.

.. code-block:: python

    whats_new_binance(symbol, interval, limit_to=-1, candles=1000)
    whats_new_yahoo(symbol, interval, limit_to=-1, candles=1000)

See every ABC, ABCD and XABCD pattern that **has formed** on an asset.  set ``limit_to=3`` to see patterns that completed within the last 3 peaks ( recommended )

.. code-block:: python

    whats_forming_binance(symbol, interval, limit_to=10, percent_complete=0.8, candles=1000)
    whats_forming_yahoo(symbol, interval, limit_to=10, percent_complete=0.8, candles=1000)

See every ABC, ABCD and XABCD pattern that **is forming** on an asset.  set ``limit_to=3`` to see patterns that completed within the last 3 peaks ( recommended )

.. code-block:: python

    whats_options_volume(symbol)
    whats_options_interest(symbol)

plots options open interest or volume for a stock.  This is very useful as it shows where the writer of the options needs the price to move to in order to limite their losses!