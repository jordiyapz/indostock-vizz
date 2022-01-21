from threading import main_thread
import pandas as pd
import numpy as np
import math
import re

from bokeh.layouts import column, gridplot
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Label, CDSView, IndexFilter, HoverTool, RangeTool, Range1d, WheelZoomTool, CrosshairTool, LinearAxis

from app.helpers.path import PATH

symbols: tuple[str] = tuple(sym for f_path in PATH.DATASET.iterdir()
                            for sym in re.findall('(\w+).JK.csv$', f_path.name))
'''List of symbols of all the available stocks.'''


class Stock:
    def __init__(self, symbol: str, width=1400):
        assert symbol in symbols, "Please provide valid symbol!"

        self.symbol = symbol
        self.df = None
        self._fig_width = width

    def load(self):
        # '''Remember! This method employs caching. Becareful!'''
        # if not self.df:
        #     self.df = pd.read_csv(PATH.DATASET/f'{self.symbol}.JK.csv',
        #                           parse_dates=['Date', ])
        '''No caching. Better 🙂'''
        return pd.read_csv(PATH.DATASET/f'{self.symbol}.JK.csv',
                           parse_dates=['Date', ])

    def __draw_main_figure(self, df, source, x_range):
        # Tools
        tooltips = [("date", "@Date{%F}"),
                    ("open", "@Open"),
                    ("high", "@High"),
                    ("low", "@Low"),
                    ("close", "@Close"),
                    ("volume", "@Volume")]
        hover_tool = HoverTool(tooltips=tooltips)
        hover_tool.formatters = {"@Date": "datetime"}
        wheel_tool = WheelZoomTool(
            dimensions='width', zoom_on_axis=True, maintain_focus=True)
        crosshair_tool = CrosshairTool(
            line_color='#0011fe', line_alpha=.8, line_width=2)

        # Figure
        fig = figure(title=f"Pergerakan Saham {self.symbol}",
                     width=self._fig_width,
                     x_axis_type="datetime",
                     x_range=x_range,
                     y_axis_location='right',
                     tools='pan, reset, help',
                     toolbar_location='left')
        fig.add_tools(hover_tool)
        fig.add_tools(wheel_tool)
        fig.add_tools(crosshair_tool)
        fig.toolbar.active_scroll = wheel_tool

        # rotate labelnya jadi 45 derajat
        fig.xaxis.major_label_orientation = math.pi/4
        # buat background grid lebih pudar
        fig.grid.grid_line_alpha = 0.3
        # sembunyikan label
        fig.xaxis.visible = False
        # fig.yaxis.major_tick_line_color = "white"
        # fig.yaxis.major_tick_in = -10
        # fig.yaxis.minor_tick_in = -3
        # fig.yaxis.minor_tick_out = 6

        # Membuat masking harga
        inc = df.Close > df.Open
        dec = df.Open > df.Close
        w = 12*60*60*1000  # half day in ms

        # Filters
        inc_view = CDSView(source=source, filters=[
                           IndexFilter(inc[inc].index)])
        dec_view = CDSView(source=source, filters=[
                           IndexFilter(dec[dec].index)])

        # Renderers
        fig.segment(x0='Date', y0='High', x1='Date',
                    y1='Low', color="black", source=source)
        fig.vbar('Date', w, 'Open', 'Close', fill_color='#00ca73',
                 line_color='black', source=source, view=inc_view)
        fig.vbar('Date', w, 'Open', 'Close', fill_color='#F2583E',
                 line_color='black', source=source, view=dec_view)

        return fig

    def __draw_range_figure(self, source, x_range, y_range):
        select = figure(plot_height=200,
                        plot_width=self._fig_width,
                        y_range=y_range,
                        x_axis_type='datetime',
                        y_axis_label='Harga per lembar',
                        tools='',
                        toolbar_location=None)

        range_tool = RangeTool(x_range=x_range)
        range_tool.overlay.fill_color = 'red'
        range_tool.overlay.fill_alpha = .2

        select.line('Date', 'Low', color='green',
                    line_width=1.5, source=source)

        # select.ygrid.gird_line_color=None
        select.add_tools(range_tool)
        select.toolbar.active_multi = range_tool

        return select

    @property
    def figure(self):
        df = self.load()
        source = ColumnDataSource(df)

        dates = np.array(df['Date'])
        x_range = Range1d(dates[-32], dates[-1])

        main_fig = self.__draw_main_figure(df, source, x_range)
        range_fig = self.__draw_range_figure(
            source, main_fig.x_range, main_fig.y_range)

        layout = column([main_fig, range_fig])
        return layout


stocks = dict(zip(symbols, map(lambda sy: Stock(sy), symbols)))
