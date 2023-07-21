pyharmonics
===========

pyharmonics detects harmonic patterns in OHLC candle data for any stock or crypto asset.  See http://www.harmonictrader.com for more information on what harmionic patterns are. In short, when a stock or crypto asset begins a price run ( moons ) the start point to the peak is considered 100% of the move. If the price drops and the amount it drops by is equal to 61.8%, 78.6% or 88.6% of the original pump, there is astrong chance a bottom will form and the price will recover.

This can happen and is respected on any time frame from 1 min to 1 month.  To know which level the price might bottom at you need to know the ABC portion of the move.  This usually involves the highest and second highest prices IF those prices peaks have a dip between them that is between 38.2% - 50% of the first pump.

See Scott Carney's Harmonic Trader books and website for more info.  There are many patterns and pyharmonics can detect them all.  It can state whether a pattern is formed or forming and it can plot those patterns.

In a pyharmonics plot.

#. Bullish patterns that have fully formed are green, bullish patterns that are still forming are yellow.
#. Bearish patterns that have fully formed are red, bearish patterns that are still forming are purple.

.. warning::
    pyharmonics is not financial advice.  It is a tool for detecting harmonic price levels or indicator divergences for an assets price trend.  Any decision taken to enter a trade on any asset is entirely yours. No risk is assumed by this API.

Installation
------------

``pip install pyharmonics``


Contents
--------

.. include:: source/marketdata.rst

.. include:: source/technicals.rst

.. include:: source/matrix.rst

.. include:: source/plot.rst