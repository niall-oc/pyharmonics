import plotly.graph_objects as go
from plotly.subplots import make_subplots

class OptionPlotter:
    def __init__(self, fundamentals, expiry):
        self.calls = fundamentals.options[expiry].calls
        self.puts = fundamentals.options[expiry].puts
        self.losses = fundamentals.options[expiry].losses
        self.expiry = expiry
        self.price = fundamentals.price
        self.symbol = fundamentals.symbol
        self.min_pain = fundamentals.options[expiry].min_pain
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
        self.plot_trend('openInterest', 1, 1)
        self.plot_price(self.price, 'Current price', 'openInterest', 1, 1)
        self.plot_trend('losses', 2, 1)
        self.plot_price(self.min_pain, 'Minimum_pain', 'losses', 2, 1)
        self.plot_price(self.price, 'Current price', 'losses', 2, 1, height=0.4)
        self.plot_losses(2, 1)

    def set_main_plot(self):
        self.main_plot = make_subplots(
            rows=2, cols=2, shared_xaxes=True,
            vertical_spacing=0.025,
            row_heights=[.5, .5], column_widths=[.9, .1]
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

    def plot_losses(self, row, col):
        self.main_plot.add_trace(
            go.Scatter(
                mode='lines+markers',
                x=self.losses['strike'],
                y=self.losses['pain'],
                fillcolor=self.colors['losses']['fill'],
                line=dict(color=self.colors['losses']['line'], width=2),
                fill='tozeroy'
            ),
            row=row, col=col
        )

    def plot_price(self, price, label, against, row, col, height=0.8):
        h = max(self.calls[against]) * height
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
                x=self.calls['strike'],
                y=self.calls[trend],
                fillcolor=self.colors['calls']['fill'],
                line=dict(color=self.colors['calls']['line'], width=2),
                fill='tozeroy'
            ),
            row=row, col=col
        )
        self.main_plot.add_trace(
            go.Scatter(
                mode='lines+markers',
                x=self.puts['strike'],
                y=self.puts[trend],
                fillcolor=self.colors['puts']['fill'],
                line=dict(color=self.colors['puts']['line'], width=2),
                fill='tozeroy'
            ),
            row=row, col=col
        )

    def show(self):
        self.main_plot.show()

class OptionSurface:
    def __init__(self, symbol, fundamentals):
        self.symbol = symbol
        self.fundamentals = fundamentals
        self.fonts = dict(
            font=dict(
                family="Courier New, monospace, bold",
                size=15
            ),
            title_font_size=30
        )

    def set_main_plot(self):
        self.main_plot = go.Figure(
            go.Surface(
                contours={
                    "x": {
                        "show": True,
                        "start": 0,  # self.fundamentals.ticker.options[0],
                        "end": len(self.fundamentals.ticker.options)  # [-1]
                    },
                    "y": {
                        "show": True,
                        "start": self.fundamentals.call_strikes[0],
                        "end": self.fundamentals.call_strikes[-1]
                    },
                },
                y=self.fundamentals.ticker.options,
                x=self.fundamentals.call_strikes,
                z=[
                    list(self.fundamentals.options[expiry].calls['openInterest'])
                    for expiry in self.fundamentals.ticker.options
                ]
            )
        )

        self.main_plot.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=False,
            title={
                'text': self.symbol,
                'y': 0.96,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            **self.fonts
        )

    def show(self):
        self.main_plot.show()
