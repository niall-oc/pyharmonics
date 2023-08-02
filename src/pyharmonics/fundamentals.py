__author__ = 'github.com/niall-oc'

import yfinance as yf

class YahooOptions:
    def __init__(self, option_chain, price, top):
        """
        :param yfinance.Ticker ticker: the yfinance Ticker object representing an asset.
        :params int top: the top 30 options, ranked by openInterest, are analyzed by default.
        """
        self.calls = option_chain.calls
        self.calls = self.calls.sort_values(by=['openInterest', 'volume'], ascending=False)[:top]
        self.calls = self.calls.sort_values(by=['strike'])
        self.calls['oi_cumsum'] = self.calls['openInterest'].cumsum()
        limit = min(self.calls['strike'])
        self.calls['losses'] = self.calls.apply(lambda row: (row['strike'] - limit) * row['oi_cumsum'], axis=1)

        self.puts = option_chain.puts
        self.puts = self.puts.sort_values(by=['openInterest', 'volume'], ascending=False)[:top]
        self.puts = self.puts.sort_values(by=['strike'])
        self.puts['oi_cumsum'] = self.puts.loc[::-1, 'openInterest'].cumsum()[::-1]
        limit = max(self.puts['strike'])
        self.puts['losses'] = self.puts.apply(lambda row: (limit - row['strike']) * row['oi_cumsum'], axis=1)

class YahooEarnings:
    def __init__(self, ticker):
        pass

class YahooFundamentals:
    def __init__(self, symbol, top=30):
        self.symbol = symbol
        self.ticker = yf.Ticker(self.symbol)
        self.options = {}
        self.price = float(self.ticker.info['currentPrice'])

    def analyse_options(self, top=30):
        """
        :params int top: the top 30 options, ranked by openInterest, are analyzed by default.
        df = df.merge(right=fun.options[fun.ticker.options[4]].calls[['strike', 'openInterest']], on='strike', how='left', suffixes=['4', f'_{fun.ticker.options[4]}'])
        """
        call_strikes = set()
        put_strikes = set()
        for expiry in self.ticker.options:
            self.options[expiry] = YahooOptions(self.ticker.option_chain(expiry), self.price, top)
            call_strikes = call_strikes | set(self.options[expiry].calls['strike'])
            put_strikes = put_strikes | set(self.options[expiry].puts['strike'])
        self.call_strikes = list(sorted(call_strikes))
        self.put_strikes = list(sorted(put_strikes))
