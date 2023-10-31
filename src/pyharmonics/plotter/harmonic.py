#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 17:02:46 2021

@author: xual
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from pyharmonics import constants, OHLCTechnicals
import pandas as pd
import datetime
import abc

class PlotterBase(abc.ABC):
    def __init__(self, technicals: OHLCTechnicals, title=None, time_horizon=None, row_map=None, colors=None, plot_ema=False, plot_sma=True, ignore_weekend=False):
        self.technicals = technicals
        self.title = title or 'chart'
        self.time_horizon = time_horizon
        self.df = technicals.df
        self.date_series = self.df.index
        self.plot_ema = plot_ema
        self.plot_sma = plot_sma
        self.ignore_weekend = ignore_weekend
        self.colors = colors or {
            constants.BEARISH: {
                constants.FORMED: {  # formed
                    'line': 'rgba(255, 127, 0, 0.6)',
                    'fill': 'rgba(255, 127, 0, 0.10)'
                },
                constants.FORMING: {  # forming
                    'line': 'rgba(200, 0, 200, 0.6)',
                    'fill': 'rgba(200, 0, 200, 0.10)'
                }
            },
            constants.BULLISH: {
                constants.FORMED: {  # formed
                    'line': 'rgba(0, 255, 0, 0.6)',
                    'fill': 'rgba(0, 255, 0, 0.10)'
                },
                constants.FORMING: {  # forming
                    'line': 'rgba(200, 200, 0, 0.6)',
                    'fill': 'rgba(200, 200, 0, 0.10)'
                }
            }
        }
        self.ROW_MAP = row_map or {
            'main': {'row': 1, 'col': 1, 'color': None, 'weight': 0.5},
            constants.VOLUME: {'row': 2, 'col': 1, 'color': None, 'weight': 0.1},
            OHLCTechnicals.MACD: {'row': 3, 'col': 1, 'color': None, 'weight': 0.1},
            OHLCTechnicals.RSI: {'row': 4, 'col': 1, 'color': 'rgba(200, 200, 0, 0.90)', 'weight': 0.1},
            OHLCTechnicals.STOCH_RSI: {'row': 5, 'col': 1, 'color': 'rgba(0, 200, 200, 0.90)', 'weight': 0.1},
            OHLCTechnicals.BBP: {'row': 6, 'col': 1, 'color': 'rgba(0, 200, 0, 0.90)', 'weight': 0.1},
        }
        self._set_candle_gap()

    def _set_candle_gap(self):
        """
        Calculates the timedelta or epoch between candles.  Important for plotting for this block of data.
        """
        scalar, vector = int(self.time_horizon[:-1]), self.time_horizon[-1:]
        times = {
            'm': {'minutes': scalar},
            'h': {'hours': scalar},
            'd': {'days': scalar},
            'w': {'days': scalar * 7},
            'M': {'days': scalar * 30}
        }
        kwargs = times[vector]
        self.candle_gap = datetime.timedelta(**kwargs)

    def _set_precision(self, p):
        self.int_precision, self.float_precision = tuple(len(c) for c in str(p).split('.'))
        digits = str(p).replace('-', '').replace('.', '')
        self.lead_zero_count = 0
        for i in digits:
            if i != 0:
                break
            self.lead_zero_count += 1

    def _price_render(self, p, currency='$'):
        if self.int_precision > 2:
            return f"{currency}{p:.2f}"
        elif self.lead_zero_count > 2:
            return f"{currency}{p:.7f}"
        else:
            return f"{currency}{p:.4f}"

    def _percent_render(self, p):
        return f"{p:.2f}%"

    def add_harmonic_plots(self, pattern_data):
        """
        """
        for family, patterns in pattern_data.items():
            for p in patterns:
                self.add_harmonic_pattern(p)

    def add_harmonic_pattern(self, p):
        """
        Publish trigger.db.HarmonicPattern objects to plots.
        """
        self._set_precision(p.completion_min_price)
        prices = p.y
        if not p.formed:
            prices[-1] = (p.completion_min_price + p.completion_max_price) / 2
        points = len(p.y)
        if points == 5:
            self._add_xabcd_pattern(p, prices)
        elif points == 4:
            self._add_abcd_pattern(p, prices)
        else:
            self._add_abc_pattern(p, prices)

    def _add_xabcd_pattern(self, p, prices):
        """
        Add a 5 point pattern to a graph. Will appear like 2 triangles in an M or W whape.

         Parameters
        ----------
        p: HarmonicPattern child
        """
        # 5 point m or w formations
        text = [
            'X',
            f'A - {p.name}',
            f"B - {p.retraces[constants.XAB]:0.3f}",
            f"C - {p.retraces[constants.ABC]:0.3f}",
            f"D - {p.retraces[constants.XABCD]:0.3f}"
        ]
        lt = p.x[0:3] + p.x[:1]
        rt = p.x[2:] + p.x[2:3]
        lp = prices[0:3] + prices[:1]
        rp = prices[2:] + prices[2:3]
        # Left Triangle ABC part
        self.main_plot.add_trace(
            go.Scatter(
                mode="lines+markers+text",
                x=lt,
                y=lp,
                fill="toself",
                fillcolor=self.colors[p.bullish][p.formed]['fill'],
                line=dict(color=self.colors[p.bullish][p.formed]['line'], width=2),
                text=text[0:3],
                textposition="top center"
            )
        )
        # Right triangle BCD part
        self.main_plot.add_trace(
            go.Scatter(
                mode="lines+markers+text",
                x=rt,
                y=rp,
                fill="toself",
                fillcolor=self.colors[p.bullish][p.formed]['fill'],
                line=dict(color=self.colors[p.bullish][p.formed]['line'], width=2),
                text=text[2:],
                textposition="top center"
            )
        )

    def add_divergence_plots(self, divergences):
        for indicator, patterns in divergences.items():
            for p in patterns:
                color = 'lightgreen' if p.bullish else '#ff7766'
                self.main_plot.add_trace(
                    go.Scatter(
                        mode="lines+markers",
                        x=p.ind_x,
                        y=p.ind_y,
                        line=dict(color=color, width=2)
                    ), row=self.ROW_MAP[p.indicator]['row'], col=self.ROW_MAP[p.indicator]['col']
                )
                self.main_plot.add_trace(
                    go.Scatter(
                        mode="lines+markers",
                        x=p.x,
                        y=p.y,
                        line=dict(color=color, width=2)
                    )
                )

    def _add_abcd_pattern(self, p, prices):
        """
        """
        text = ["A", f"B - {p.name}", f"C - {p.retraces[constants.ABC]:0.3f}", f"D - {p.retraces[constants.BCD]:0.3f}"]
        line = dict(color=self.colors[p.bullish][p.formed]['line'], width=3)
        self.main_plot.add_trace(
            go.Scatter(
                mode="lines+text",
                x=p.x,
                y=prices,
                line=line,
                text=text,
                textposition="bottom center"
            )
        )

    def _add_abc_pattern(self, p, prices):
        """
        """
        text = ['', '', f"{'long' if p.bullish else 'short'} {p.name}"]
        line = dict(color=self.colors[p.bullish][p.formed]['line'], width=2, dash='dash')
        self.main_plot.add_trace(
            go.Scatter(
                mode="lines+text",
                x=p.x,
                y=prices,
                line=line,
                text=text,
                textposition="bottom center"
            )
        )

    def add_peaks(self):
        self.main_plot.add_trace(
            go.Scatter(
                mode="markers",
                x=self.df.index.values[self.technicals.lows],
                y=[i[1] for i in self.technicals.peak_data if not i[2]],
                line=dict(color='lightgreen', width=1)
            )
        )

        self.main_plot.add_trace(
            go.Scatter(
                mode="markers",
                x=self.df.index.values[self.technicals.highs],
                y=[i[1] for i in self.technicals.peak_data if i[2]],
                line=dict(color='#ff7766', width=1)
            )
        )

        for indicator in (self.technicals.MACD_PEAKS, self.technicals.RSI_PEAKS):
            x, y = self.technicals.get_peak_x_y(indicator)
            row = indicator.split('_')[0]
            self.main_plot.add_trace(
                go.Scatter(
                    mode="markers",
                    x=self.technicals.get_index_x(x),
                    y=y,
                    line=dict(color='#ff7766', width=1)
                ),
                row=self.ROW_MAP[row]['row'],
                col=self.ROW_MAP[row]['col'],
            )

        for indicator in (self.technicals.MACD_DIPS, self.technicals.RSI_DIPS):
            x, y = self.technicals.get_peak_x_y(indicator)
            row = indicator.split('_')[0]
            self.main_plot.add_trace(
                go.Scatter(
                    mode="markers",
                    x=self.technicals.get_index_x(x),
                    y=y,
                    line=dict(color='lightgreen', width=1)
                ),
                row=self.ROW_MAP[row]['row'],
                col=self.ROW_MAP[row]['col'],
            )

    def add_volume_plot(self):
        """
        """
        row = self.ROW_MAP[constants.VOLUME]['row']
        col = self.ROW_MAP[constants.VOLUME]['col']
        color = [
            'lightgreen' if row[constants.OPEN] - row[constants.CLOSE] >= 0 else '#ff7766'
            for _, row in self.df.iterrows()
        ]
        self.main_plot.add_trace(
            go.Bar(
                x=self.date_series,
                y=self.df[constants.VOLUME],
                marker_color=color
            ),
            row=row, col=col
        )
        self.main_plot.update_yaxes(title_text=constants.VOLUME, row=row, col=col)

    def add_macd_plot(self):
        # Plot MACD trace on 3rd row
        row = self.ROW_MAP[self.technicals.MACD]['row']
        col = self.ROW_MAP[self.technicals.MACD]['col']
        # Plot bullish div
        # macd_min = np.nanmin(self.df[constants.MACD])
        # bull_y = [macd_min * i for i in self.technicals.divergences[constants.MACD][constants.BULLISH]]
        # self.main_plot.add_trace(go.Bar(x=self.date_series, y=bull_y, marker_color=self.colors[constants.BULLISH][constants.FORMED]['line']), row=row, col=col)
        # plot bearish div
        # macd_max = np.nanmax(self.df[constants.MACD])
        # bear_y = [macd_max * i for i in self.technicals.divergences[constants.MACD][constants.BEARISH]]
        # self.main_plot.add_trace(go.Bar(x=self.date_series, y=bear_y, marker_color=self.colors[constants.BEARISH][constants.FORMED]['line']), row=row, col=col)
        # plot MACD
        color = [
            'lightgreen' if val >= 0 else '#ff7766'
            for val in self.technicals.indicators[self.technicals.MACD]
        ]
        self.main_plot.add_trace(
            go.Bar(
                x=self.date_series,
                y=self.df[self.technicals.MACD],
                marker_color=color
            ),
            row=row, col=col
        )
        self.main_plot.update_yaxes(title_text=self.technicals.MACD, showgrid=False, row=row, col=1)

    def add_indicator_plot(self, ind):
        row = self.ROW_MAP[ind]['row']
        col = self.ROW_MAP[ind]['col']
        # Plot bullish div
        # ind_max = np.nanmax(self.df[ind])
        # ind_min = ind_max / 2
        # bull_y = [ind_min * i for i in self.technicals.divergences[ind][constants.BULLISH]]
        # self.main_plot.add_trace(go.Bar(x=self.date_series, y=bull_y, marker_color=self.colors[constants.BULLISH][constants.FORMED]['line']), row=row, col=col)
        # plot bearish div
        # bear_y = [ind_max * i for i in self.technicals.divergences[ind][constants.BEARISH]]
        # self.main_plot.add_trace(go.Bar(x=self.date_series, y=bear_y, marker_color=self.colors[constants.BEARISH][constants.FORMED]['line'], ), row=row, col=col)
        self.main_plot.add_trace(
            go.Scatter(
                x=self.date_series,
                y=self.df[ind],
                line=dict(color=self.ROW_MAP[ind]['color'], width=2)
            ),
            row=row, col=col
        )
        self.main_plot.update_yaxes(title_text=ind, row=row, col=col)

    def remove_date_gaps(self):
        self.main_plot.update_xaxes(rangebreaks=[
            dict(bounds=['sat', 'mon']),
            dict(bounds=[21, 14.5], pattern='hour'),
            # dict(values=["2022-11-24", "2022-12-25", "2023-01-01"])
        ])

    def _create_main_plot(self):
        if isinstance(self.technicals, OHLCTechnicals):
            self.main_plot.add_trace(
                go.Candlestick(
                    x=self.date_series,
                    open=self.df[constants.OPEN],
                    high=self.df[constants.HIGH],
                    close=self.df[constants.CLOSE],
                    low=self.df[constants.LOW],
                ),
                row=self.ROW_MAP['main']['row'], col=self.ROW_MAP['main']['col']
            )
        else:
            self.main_plot.add_trace(
                go.Scatter(
                    x=self.date_series,
                    y=self.df[constants.CLOSE]
                ),
                row=self.ROW_MAP['main']['row'], col=self.ROW_MAP['main']['col']
            )

    def set_main_plot(self):
        self._create_main_plot()
        if self.plot_ema:
            self.main_plot.add_trace(go.Scatter(x=self.date_series, y=self.df[self.technicals.EMA_5], line=dict(color='rgba(64, 64, 255, 1)', width=1)))
            self.main_plot.add_trace(go.Scatter(x=self.date_series, y=self.df[self.technicals.EMA_8], line=dict(color='rgba(64, 255, 255, 1)', width=1)))
            self.main_plot.add_trace(go.Scatter(x=self.date_series, y=self.df[self.technicals.EMA_13], line=dict(color='rgba(64, 255, 64, 1)', width=1)))
            self.main_plot.add_trace(go.Scatter(x=self.date_series, y=self.df[self.technicals.EMA_21], line=dict(color='rgba(255, 255, 64, 1)', width=1)))
            self.main_plot.add_trace(go.Scatter(x=self.date_series, y=self.df[self.technicals.EMA_34], line=dict(color='rgba(255, 128, 64, 1)', width=1)))
            self.main_plot.add_trace(go.Scatter(x=self.date_series, y=self.df[self.technicals.EMA_55], line=dict(color='rgba(255, 64, 64, 1)', width=1)))
        if self.plot_sma:
            self.main_plot.add_trace(go.Scatter(x=self.date_series, y=self.df[self.technicals.SMA_50], line=dict(color='rgba(64, 64, 64, 0.5)', width=2)))
            self.main_plot.add_trace(go.Scatter(x=self.date_series, y=self.df[self.technicals.SMA_100], line=dict(color='rgba(128, 128, 128, 0.5)', width=2)))
            self.main_plot.add_trace(go.Scatter(x=self.date_series, y=self.df[self.technicals.SMA_150], line=dict(color='rgba(200, 200, 200, 0.5)', width=2)))
            self.main_plot.add_trace(go.Scatter(x=self.date_series, y=self.df[self.technicals.SMA_200], line=dict(color='rgba(255, 255, 255, 0.5)', width=2)))
        self.main_plot.update_yaxes(title_text=self.title)
        self.main_plot.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=False,
            title={
                'text': self.plot_title,
                'y': 0.96,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            **self.fonts
        )

    def show(self):
        self.main_plot.show()

    def save_plot_image(self, location, dpi=600):
        if self.ignore_weekend:
            self.main_plot.update_xaxes(
                rangebreaks=[
                    dict(bounds=['sat', 'mon']),
                    dict(bounds=[21, 14.5], pattern='hour'),
                ]
            )
        pio.write_image(self.main_plot, f"{location}", width=4 * dpi, height=2 * dpi, scale=1)


class HarmonicPlotter(PlotterBase):
    def __init__(self, technicals: OHLCTechnicals, row_map=None, colors=None, plot_ema=False, plot_sma=True):
        super(HarmonicPlotter, self).__init__(technicals, title=technicals.symbol, time_horizon=technicals.interval,
                                              row_map=row_map, colors=colors, plot_ema=plot_ema, plot_sma=plot_sma)
        self.plot_title = f"{self.title} {self.time_horizon}"
        self.fonts = dict(
            font=dict(
                family="Courier New, monospace, bold",
                size=15
            ),
            title_font_size=38
        )
        self.set_sub_plots()
        self.set_main_plot()
        self.add_volume_plot()

        for ind in self.technicals.indicators:
            if ind == self.technicals.MACD:
                self.add_macd_plot()
            else:
                self.add_indicator_plot(ind)

    def set_sub_plots(self):
        space = 1 - (self.ROW_MAP['main']['weight'] + self.ROW_MAP[constants.VOLUME]['weight'])
        indicator_height = space / len(self.technicals.indicators)
        heights = [self.ROW_MAP['main']['weight'], self.ROW_MAP[constants.VOLUME]['weight']] + [indicator_height for _ in self.technicals.indicators]
        self.main_plot = make_subplots(
            rows=len(heights), shared_xaxes=True,
            vertical_spacing=0.025,
            row_heights=heights
        )

class Plotter(PlotterBase):
    def __init__(self, technicals: OHLCTechnicals, row_map=None, colors=None, plot_ema=False, plot_sma=True):
        super(Plotter, self).__init__(technicals, title=technicals.symbol, time_horizon=technicals.interval, row_map=row_map, colors=colors, plot_ema=plot_ema, plot_sma=plot_sma)
        self.plot_title = f"{self.title} {self.time_horizon}"
        self.fonts = dict(
            font=dict(
                family="Courier New, monospace, bold",
                size=15
            ),
            title_font_size=38
        )
        self.ROW_MAP = row_map or {
            'main': {'row': 1, 'col': 1, 'color': None, 'weight': 0.5},
            OHLCTechnicals.MACD: {'row': 2, 'col': 1, 'color': None, 'weight': 0.125},
            OHLCTechnicals.RSI: {'row': 3, 'col': 1, 'color': 'rgba(200, 200, 0, 0.90)', 'weight': 0.125},
            OHLCTechnicals.STOCH_RSI: {'row': 4, 'col': 1, 'color': 'rgba(0, 200, 200, 0.90)', 'weight': 0.125},
            OHLCTechnicals.BBP: {'row': 5, 'col': 1, 'color': 'rgba(0, 200, 0, 0.90)', 'weight': 0.125},
        }
        self.set_sub_plots()
        self.set_main_plot()

        for ind in self.technicals.indicators:
            if ind == self.technicals.MACD:
                self.add_macd_plot()
            else:
                self.add_indicator_plot(ind)

    def set_sub_plots(self):
        space = 1 - (self.ROW_MAP['main']['weight'])
        indicator_height = space / len(self.technicals.indicators)
        heights = [self.ROW_MAP['main']['weight']] + [indicator_height for _ in self.technicals.indicators]
        self.main_plot = make_subplots(
            rows=len(heights), shared_xaxes=True,
            vertical_spacing=0.025,
            row_heights=heights
        )


class PositionPlotter(PlotterBase):
    def __init__(self, technicals, position, row_map=None, colors=None, plot_ema=False, plot_sma=True):
        super(PositionPlotter, self).__init__(technicals, title=position.symbol, time_horizon=position.pattern.interval,
                                              row_map=row_map, colors=colors, plot_ema=plot_ema, plot_sma=plot_sma)
        self.plot_title = f"{self.title} {self.time_horizon} - price: {technicals.spot:.4f}"
        self.fonts = dict(
            font=dict(
                family="Courier New, monospace, bold",
                size=15
            ),
            title_font_size=30
        )
        self.position = position
        self.set_sub_plots()
        self.set_main_plot()
        self.add_volume_plot()

        for ind in self.technicals.indicators:
            if ind == self.technicals.MACD:
                self.add_macd_plot()
            else:
                self.add_indicator_plot(ind)
        self._set_position()

    def set_sub_plots(self):
        space = 1 - (self.ROW_MAP['main']['weight'] + self.ROW_MAP[constants.VOLUME]['weight'])
        indicator_height = space / len(self.technicals.indicators)
        heights = [self.ROW_MAP['main']['weight'], self.ROW_MAP[constants.VOLUME]['weight']] + [indicator_height for _ in self.technicals.indicators]
        self.main_plot = make_subplots(
            rows=len(heights), cols=2, shared_xaxes=True,
            vertical_spacing=0.025,
            row_heights=heights,
            column_widths=[0.66, 0.33]
        )

    def _add_pattern_completion_zone(self, candle_width, chart_end_time):
        # Add target completion zone
        self.main_plot.add_trace(
            go.Scatter(
                mode="markers+lines+text",
                x=[chart_end_time, chart_end_time + candle_width, chart_end_time + candle_width, chart_end_time, chart_end_time],
                y=[
                    self.position.pattern.completion_min_price,
                    self.position.pattern.completion_min_price,
                    self.position.pattern.completion_max_price,
                    self.position.pattern.completion_max_price,
                    self.position.pattern.completion_min_price
                ],
                fillcolor='rgba(200, 200, 200, 0.075)',
                text=["", "", "", "Entry->        "],
                fill="toself",
                line=dict(color='rgba(200, 200, 200, 0.85)', width=1)
            )
        )

    def _add_price_target_blocks(self, target_block_width, chart_end_time):
        target_candle = chart_end_time + target_block_width
        is_stop = not self.position.pattern.bullish
        i = 1
        for target in self.position.targets:
            # Profit Rectangle
            self.main_plot.add_trace(
                go.Scatter(
                    mode="lines+text",
                    x=[target_candle, target_candle + target_block_width, target_candle + target_block_width, target_candle, target_candle],
                    y=[self.position.strike, self.position.strike, target, target, self.position.strike],
                    fillcolor=self.colors[self.position.pattern.bullish][self.position.pattern.formed]['fill'],
                    fill="toself",
                    text=["", "", f"T{i}", ""],
                    line=dict(color=self.colors[self.position.pattern.bullish][self.position.pattern.formed]['line'], width=1)
                )
            )
            # Loss Rectangle
            self.main_plot.add_trace(
                go.Scatter(
                    mode="lines+text",
                    x=[target_candle, target_candle + target_block_width, target_candle + target_block_width, target_candle, target_candle],
                    y=[self.position.strike, self.position.strike, self.position.stop, self.position.stop, self.position.strike],
                    fillcolor=self.colors[is_stop][self.position.pattern.formed]['fill'],
                    fill="toself",
                    text=["", "", "Stop", ""],
                    line=dict(color=self.colors[is_stop][self.position.pattern.formed]['line'], width=1)
                )
            )
            i += 1
            target_candle = target_candle + target_block_width + target_block_width

    def _add_position_outcomes(self):
        """
        """
        num_targets = len(self.position.targets)
        title_col = ['Stop', 'Strike']
        price_col = [f"{self._price_render(self.position.stop)}", f"{self._price_render(self.position.strike)}"]
        move_col = [f"{(self.position.moves['stop']-1) * 100:0.3f}%", "0.00%"]
        position_col_base = [f"${self.position.outcomes['stop']:.2f}", f"${self.position.outcomes['position_size']:.2f}"]
        position_cols = []
        total_col = [
            self.position.outcomes['stop'] * num_targets,
            self.position.dollar_amount,
        ]
        totals = [self.position.outcomes['stop'] for t in self.position.targets]
        for i, t in enumerate(self.position.targets, 1):
            key = f't{i}'
            title_col.append(f'Target {i}')
            price_col.append(f"{self._price_render(t)}")
            move_col.append(f"{(self.position.moves[key]-1) * 100:.3f}%")
            positions_cells = [f"${self.position.outcomes[key]:.2f}" if c >= i else f"${self.position.outcomes['stop']:.2f}" for c in range(num_targets)]
            positions_cells[i - 1] = f"${self.position.outcomes[key]:.2f}"
            position_cols.append(position_col_base + positions_cells)
            totals[i - 1] = self.position.outcomes[key]
            total_col.append(sum(totals))

        # COLORS
        red = 'rgb(50, 0, 0)'
        black = 'black'
        green = 'rgb(0, 50, 0)'
        fill_color = [
            [red, black] + [green for t in self.position.targets],
            [red, black] + [green for t in self.position.targets],
            [red, black] + [green for t in self.position.targets],
        ]
        for i in range(num_targets):
            positions_colors = [red if c < i else green for c in range(num_targets)]
            fill_color.append(
                [red, black] + positions_colors
            )
        fill_color.append([red, black] + [green for t in self.position.targets])

        # Reverse colors for long
        if self.position.long:
            title_col.reverse()
            price_col.reverse()
            move_col.reverse()
            position_cols = [p[::-1] for p in position_cols]
            fill_color = [f[::-1] for f in fill_color]
            total_col.reverse()

        total_col = [f"${t:.2f}" for t in total_col]

        data_cells = [title_col, price_col, move_col] + position_cols + [total_col]
        headers = ['Limit', 'Price', '%Move'] + [f'Pos {i+1}' for i in range(num_targets)] + ['Returns']
        widths = [20, 19, 17] + [17 for _ in position_cols] + [20]

        self.main_plot.add_trace(
            go.Table(
                domain=dict(
                    x=[0.63, 1],
                    y=[0.95, 1]
                ),
                header=dict(
                    values=[f'Trade Outcomes for ${self.position.dollar_amount} position'],
                    fill_color='darkslategray',
                    font=dict(color=['rgb(255, 255, 255)'] * len(data_cells), size=25),
                    height=60
                )
            )
        )

        self.main_plot.add_trace(
            go.Table(
                domain=dict(
                    x=[0.63, 1],
                    y=[0.37, 0.95]
                ),
                columnwidth=widths,
                header=dict(
                    values=headers,
                    fill_color='black',
                    font=dict(color=['rgb(245, 245, 245)'] * len(data_cells), size=18),
                    height=40
                ),
                cells=dict(
                    values=data_cells,
                    line_color='darkslategray',
                    fill_color=fill_color,
                    align='left',
                    font=dict(color=['rgb(245, 245, 145)'] * len(data_cells), size=14),
                    height=35,
                )
            )
        )

    def _set_position(self, shape_width=0.1):
        """
        """
        self._set_precision(self.position.strike)
        # Add padding for target
        target_block_width = self.candle_gap * int(len(self.df) * shape_width)
        chart_end_time = self.position.pattern.x[-1]
        final_candle = self.technicals.df.index[-1]
        if not self.position.pattern.formed:
            self.pad_right(final_candle)
            chart_end_time = final_candle - (self.candle_gap * 3)

        self.add_harmonic_pattern(self.position.pattern)
        self._add_pattern_completion_zone(target_block_width, chart_end_time)
        self._add_price_target_blocks(target_block_width, chart_end_time)
        self._add_position_outcomes()

        self.plot_title = f"{self.plot_title}-{self.time_horizon}" + \
                          f" --- {'Long' if self.position.long else 'Short'} Entry: {self._price_render(self.position.strike)}"

    def pad_right(self, final_candle, num_candles=120):
        """
        """
        cols = self.df.columns
        this_time = final_candle
        data = []
        for i in range(num_candles):
            this_time += self.candle_gap
            row = [this_time if c == self.candle_data.df_index else None for c in cols]
            data.append(row)
        pad_df = pd.DataFrame(data, columns=cols)
        pad_df[constants.INDEX] = pad_df[self.candle_data.df_index]
        pad_df = pad_df.set_index(pad_df[constants.INDEX])
        self.df = pd.concat([self.df, pad_df])
