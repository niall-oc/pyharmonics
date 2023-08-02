import plotly.graph_objects as go
from plotly.subplots import make_subplots

class OptionPlotter:
    def __init__(self, symbol, expiry, options, price):
        self.calls = options.calls
        self.puts = options.puts
        self.expiry = expiry
        self.price = price
        self.symbol = symbol
        self.fonts = dict(
            font=dict(
                family="Courier New, monospace, bold",
                size=15
            ),
            title_font_size=30
        )
        self.title = f"{self.symbol} - {self.expiry}"
        self.set_main_plot()
        self.plot_trend('openInterest', 1)
        self.plot_trend('losses', 2)

    def set_main_plot(self):
        self.main_plot = make_subplots(
            rows=2, shared_xaxes=True,
            vertical_spacing=0.025,
            row_heights=[.5, .5]
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

    def plot_current_price(self):
        self.main_plot.add_trace(
            go.Scatter(
                mode='lines+text',
                x=[self.price * .999, self.price],
                y=[max(self.calls['openInterest']) * 0.8, max(self.calls['openInterest']) * 0.8],
                line=dict(color='white', width=2),
                fill='tozeroy',
                text=['', f"Current Price: {self.price}"]
            ),
            row=1, col=1
        )

    def plot_trend(self, trend, row):
        self.main_plot.add_trace(
            go.Scatter(
                x=self.calls['strike'],
                y=self.calls[trend],
                line=dict(color='lightgreen', width=2),
                fill='tozeroy'
            ),
            row=row, col=1
        )
        self.main_plot.add_trace(
            go.Scatter(
                x=self.puts['strike'],
                y=self.puts[trend],
                line=dict(color='red', width=2),
                fill='tozeroy'
            ),
            row=row, col=1
        )
        self.main_plot.add_trace(
            go.Scatter(
                mode='lines+text',
                x=[self.price * .999, self.price],
                y=[max(self.calls[trend]) * 0.8, max(self.calls[trend]) * 0.8],
                line=dict(color='white', width=2),
                fill='tozeroy',
                text=['', f"Current Price: {self.price}"]
            ),
            row=row, col=1
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
