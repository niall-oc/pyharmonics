__author__ = 'github.com/niall-oc'

import yfinance as yf

class YahooOptions:
    def __init__(self, option_chain, top):
        """
        :param yfinance.Ticker ticker: the yfinance Ticker object representing an asset.
        :params int top: the top 30 options, ranked by openInterest, are analyzed by default.
        """
        self.calls = option_chain.calls
        self.calls = self.calls.sort_values(by=['openInterest', 'volume'], ascending=False)[:top]
        self.calls = self.calls.sort_values(by=['strike'])
        self.calls['oi_cumsum'] = self.calls['openInterest'].cumsum()
        limit = min(self.calls['strike'])
        self.calls['losses'] = self.calls.apply(lambda row: (row['strike'] - limit) * row['oi_cumsum'] * 100, axis=1)

        self.puts = option_chain.puts
        self.puts = self.puts.sort_values(by=['openInterest', 'volume'], ascending=False)[:top]
        self.puts = self.puts.sort_values(by=['strike'])
        self.puts['oi_cumsum'] = self.puts.loc[::-1, 'openInterest'].cumsum()[::-1]
        limit = max(self.puts['strike'])
        self.puts['losses'] = self.puts.apply(lambda row: (limit - row['strike']) * row['oi_cumsum'] * 100, axis=1)

        pain_df = self.calls[['strike', 'losses']].merge(self.puts[['strike', 'losses']], on='strike', how='outer').sort_values(by='strike')
        pain_df['losses_x'] = pain_df['losses_x'].fillna(0.0)
        pain_df['losses_y'] = pain_df['losses_y'].fillna(0.0)
        pain_df['pain'] = pain_df.apply(lambda x: x['losses_x'] + x['losses_y'], axis=1)
        self.min_pain = list(pain_df.loc[pain_df['pain'] == min(pain_df['pain'])].to_dict()['strike'].values())[0]
        self.losses = pain_df

class YahooEarnings:
    def __init__(self, ticker):
        pass

class YahooFundamentals:
    def __init__(self, symbol):
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
            self.options[expiry] = YahooOptions(self.ticker.option_chain(expiry), top)
            call_strikes = call_strikes | set(self.options[expiry].calls['strike'])
            put_strikes = put_strikes | set(self.options[expiry].puts['strike'])
        self.call_strikes = list(sorted(call_strikes))
        self.put_strikes = list(sorted(put_strikes))
