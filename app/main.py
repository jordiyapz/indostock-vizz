from dotenv import dotenv_values
import pandas as pd
import math

from bokeh.plotting import figure, curdoc

from app.helpers.stock import Stock
from .helpers import download_data, PATH


config = dotenv_values('.env')

fig = Stock('EXCL').figure

curdoc().theme = 'dark_minimal'
curdoc().add_root(fig)
