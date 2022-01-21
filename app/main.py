from dotenv import dotenv_values
from bokeh.plotting import curdoc
from bokeh.layouts import column, row, Spacer
from bokeh.models import Select, Div

from app.helpers.stock import Stock, symbols


def create_root(main):
    '''Template untuk membangun root file. Root terdiri atas header dan main.'''
    title = Div(text='<h1>IndoStock Vizzard</h1>')
    header = row([title, Spacer(), select_el], sizing_mode='stretch_width')
    return column([header, main], sizing_mode='stretch_width')


def on_change(attr, old, new):
    new_fig = Stock(new).figure
    document.clear()
    document.add_root(create_root(new_fig))
    document.title = f'{new} | IndoStock Vizzard'


config = dotenv_values('.env')

initial_symbol = 'TLKM'

document = curdoc()
document.theme = 'dark_minimal'
document.title = f'{initial_symbol} | IndoStock Vizzard'


fig = Stock(initial_symbol).figure
select_el = Select(title="Kode", value=initial_symbol, options=list(symbols))

select_el.on_change('value', on_change)

document.add_root(create_root(fig))
