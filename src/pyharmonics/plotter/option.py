import plotly.graph_objects as go
from plotly.subplots import make_subplots

class OptionPlotterBase:
    def __init__(self, ticker, top=30):
        self.ticker = ticker
        self.fonts = dict(
            font=dict(
                family="Courier New, monospace, bold",
                size=15
            ),
            title_font_size=30
        )
        self.analyse_options(top=top)
        self.set_main_plot()
        self.plot_open_interest()
        self.plot_current_price()

    def analyse_options(self, top=30):
        self.oc = self.ticker.option_chain()
        self.price = self.ticker.info['currentPrice']
        self.calls = self.oc.calls
        self.puts = self.oc.puts
        self.title = self.ticker.info['symbol']
        self.calls['expiryDate'] = self.calls['contractSymbol'].map(lambda x: x.split('C')[0].split(self.title))
        self.puts['expiryDate'] = self.puts['contractSymbol'].map(lambda x: x.split('C')[0].split(self.title))

        self.title = f"{self.title} - {self.calls['expiryDate'][0][1]}"
        self.calls = self.calls.sort_values(by=['openInterest', 'volume'], ascending=False)[:top]
        self.calls = self.calls.sort_values(by=['strike'])
        self.puts = self.puts.sort_values(by=['openInterest', 'volume'], ascending=False)[:top]
        self.puts = self.puts.sort_values(by=['strike'])

    def set_main_plot(self):
        self.main_plot = make_subplots(
            rows=1, shared_xaxes=True,
            vertical_spacing=0.025,
            row_heights=[1]
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

    def plot_open_interest(self):
        self.main_plot.add_trace(
            go.Scatter(
                x=self.calls['strike'],
                y=self.calls['openInterest'],
                line=dict(color='lightgreen', width=2),
                fill='tozeroy'
            ),
            row=1, col=1
        )
        self.main_plot.add_trace(
            go.Scatter(
                x=self.puts['strike'],
                y=self.puts['openInterest'],
                line=dict(color='red', width=2),
                fill='tozeroy'
            ),
            row=1, col=1
        )

    def show(self):
        self.main_plot.show()

class OptionPlotter(OptionPlotterBase):
    pass
