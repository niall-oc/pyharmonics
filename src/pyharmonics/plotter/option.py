import plotly.graph_objects as go
from plotly.subplots import make_subplots

class OptionPlotter:
    def __init__(self, yo, expiry):
        """
        :param pyharmonics.marketdata.YahooOptions yo: Option chain data for an asset
        :param str expiry: Must be one of the expiry dates in yo.ticker.options
        """
        self.yo = yo
        self.options = yo.options[expiry]
        self.expiry = expiry
        self.price = yo.price
        self.symbol = yo.symbol
        self.min_pain = self.options.min_pain
        self.fonts = dict(
            font=dict(
                family="Courier New, monospace, bold",
                size=15
            ),
            title_font_size=30
        )
        self.colors = {
            'calls': {  # formed
                'line': 'rgba(0, 255, 0, 0.6)',
                'fill': 'rgba(0, 255, 0, 0.15)'
            },
            'puts': {  # forming
                'line': 'rgba(255, 127, 0, 0.6)',
                'fill': 'rgba(255, 127, 0, 0.15)'
            },
            'losses': {
                'line': 'rgba(255, 255, 255, 0.6)',
                'fill': 'rgba(255, 255, 255, 0.05)',
            }
        }
        self.title = f"{self.symbol} - {self.expiry}"
        self.set_main_plot()

    def set_main_plot(self):
        self.main_plot = make_subplots(
            rows=2, cols=2, shared_xaxes=False,
            vertical_spacing=0.1,
            row_heights=[.5, .4], column_widths=[.6, .4]
        )
        self.main_plot.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=False,
            title={
                'text': self.title,
                'y': 0.96,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            **self.fonts
        )
        # Main options data
        self.plot_trend(self.options.trend, 1, 1)
        self.plot_price(self.price, 'Current price', self.options.trend, 1, 1)
        self.main_plot.update_xaxes(title_text=f'Option {self.options.trend}', row=1, col=1)
        self.main_plot.update_yaxes(title_text=f'Option {self.options.trend}', row=1, col=1)
        # Max pain for this date
        self.plot_trend('losses', 2, 1)
        self.plot_price(self.options.min_pain, 'Minimum_pain', 'losses', 2, 1)
        self.plot_price(self.price, 'Current price', 'losses', 2, 1, height=0.4)
        self.main_plot.update_xaxes(title_text=f'Max Pain {self.options.trend}', row=2, col=1)
        self.main_plot.update_yaxes(title_text=f'Max Pain {self.options.trend}', row=2, col=1)
        # Forward looking pain
        self.plot_losses(2, 1)
        self.plot_pain(1, 2)
        self.main_plot.update_xaxes(title_text='Forward looking pain', row=1, col=2)

    def plot_pain(self, row, col):
        self.main_plot.add_trace(
            go.Scatter(
                mode='lines+markers',
                x=self.yo.ticker.options,
                y=[self.yo.options[d].min_pain for d in self.yo.ticker.options],
                fillcolor=self.colors['losses']['fill'],
                line=dict(color=self.colors['losses']['line'], width=2),
                fill='tozeroy'
            ),
            row=row, col=col
        )
        self.main_plot.add_trace(
            go.Scatter(
                mode='lines+markers+text',
                y=[self.price, self.price],
                x=[self.yo.ticker.options[0], self.yo.ticker.options[-2]],
                line=dict(color='white', width=1),
                text=['', f"spot: {self.price}"],
                textposition="top center"
            ),
            row=row, col=col
        )

    def plot_losses(self, row, col):
        self.main_plot.add_trace(
            go.Scatter(
                mode='lines+markers',
                x=self.options.losses['strike'],
                y=self.options.losses['pain'],
                fillcolor=self.colors['losses']['fill'],
                line=dict(color=self.colors['losses']['line'], width=2),
                fill='tozeroy'
            ),
            row=row, col=col
        )

    def plot_price(self, price, label, against, row, col, height=0.8):
        h = (max(self.options.calls[against]) + max(self.options.puts[against])) * height / 2
        self.main_plot.add_trace(
            go.Scatter(
                mode='lines+markers+text',
                x=[price * .9999, price],
                y=[h, h],
                line=dict(color='white', width=2),
                fill='tozeroy',
                text=['', f"{label}: {price}"],
                textposition="top center"
            ),
            row=row, col=col
        )

    def plot_trend(self, trend, row, col):
        self.main_plot.add_trace(
            go.Scatter(
                mode='lines+markers',
                x=self.options.calls['strike'],
                y=self.options.calls[trend],
                fillcolor=self.colors['calls']['fill'],
                line=dict(color=self.colors['calls']['line'], width=2),
                fill='tozeroy'
            ),
            row=row, col=col
        )
        self.main_plot.add_trace(
            go.Scatter(
                mode='lines+markers',
                x=self.options.puts['strike'],
                y=self.options.puts[trend],
                fillcolor=self.colors['puts']['fill'],
                line=dict(color=self.colors['puts']['line'], width=2),
                fill='tozeroy'
            ),
            row=row, col=col
        )

    def show(self):
        self.main_plot.show()

class OptionSurface:
    def __init__(self, yo):
        self.yo = yo
        self.fonts = dict(
            font=dict(
                family="Courier New, monospace, bold",
                size=15
            ),
            title_font_size=30
        )
        self.call_strikes = set()
        self.put_strikes = set()
        for expiry, options in self.yo.options.items():
            self.call_strikes = self.call_strikes | set(options.calls['strike'])
            self.put_strikes = self.put_strikes | set(options.puts['strike'])

    def set_main_plot(self):
        self.main_plot = go.Figure(
            go.Surface(
                contours={
                    "x": {
                        "show": True,
                        "start": 0,  # self.fundamentals.ticker.options[0],
                        "end": len(self.yo.ticker.options)  # [-1]
                    },
                    "y": {
                        "show": True,
                        "start": self.call_strikes[0],
                        "end": self.call_strikes[-1]
                    },
                },
                y=self.yo.ticker.options,
                x=self.call_strikes,
                z=[
                    list(self.yo.options[expiry].calls['openInterest'])
                    for expiry in self.yo.ticker.options
                ]
            )
        )

        self.main_plot.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=False,
            title={
                'text': self.yo.symbol,
                'y': 0.96,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            **self.fonts
        )

    def show(self):
        self.main_plot.show()
