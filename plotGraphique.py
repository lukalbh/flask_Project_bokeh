from bokeh.plotting import figure
from database import DBconnection
import numpy as np

from bokeh.embed import components

def create_bar_chart():
    x = ['A', 'B', 'C', 'D', 'E']
    y = [12, 19, 3, 5, 2]
    
    plot = figure(x_range=x, title="Graphique en Barres", toolbar_location=None, tools="",
                  width=600, height=400)  # Dimensions agrandies
    plot.vbar(x=x, top=y, width=0.9, color="blue")
    plot.xgrid.grid_line_color = None
    plot.y_range.start = 0
    plot.xaxis.axis_label = 'Catégories'
    plot.yaxis.axis_label = 'Valeurs'
    
    script, div = components(plot)
    return script, div

def create_line_chart():
    x = np.linspace(0, 4 * np.pi, 100)
    y = np.sin(x)
    
    plot = figure(title="Graphique Linéaire", x_axis_label='x', y_axis_label='sin(x)',
                  width=600, height=400)  # Dimensions agrandies
    plot.line(x, y, line_width=2)
    
    script, div = components(plot)
    return script, div

def create_pie_chart():
    categories = ['Red', 'Blue', 'Yellow', 'Green']
    values = [12, 19, 3, 5]

    plot = figure(title="Graphique Circulaire", tools="hover", tooltips="@categories: @values", 
                  x_range=(-1, 1), y_range=(-1, 1), width=600, height=400)  # Dimensions agrandies
    plot.wedge(x=0, y=0, radius=0.4, start_angle=0, end_angle=values, fill_color="color")
    
    script, div = components(plot)
    return script, div
