from datetime import date, timedelta
import pandas as pd
from bokeh.models import ColumnDataSource, DateSlider, CustomJS
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.embed import components

def create_date_slider_plot():
    # Simulation de données : 10 jours de température
    dates = [date(2024, 5, 1) + timedelta(days=i) for i in range(10)]
    temperatures = [18, 19, 20, 21, 19, 18, 22, 23, 21, 20]

    df = pd.DataFrame({"date": dates, "temp": temperatures})

    # Les dates doivent être converties en format JavaScript (timestamp) pour CustomJS
    df["date"] = pd.to_datetime(df["date"])
    df["date_ms"] = df["date"].astype('int64') // 10**6  # JS utilise des ms

    source = ColumnDataSource(data=dict(date=df["date"], temp=df["temp"]))
    original = ColumnDataSource(data=dict(date=df["date"], temp=df["temp"], date_ms=df["date_ms"]))

    # Graphique Bokeh
    p = figure(x_axis_type="datetime", title="Température quotidienne", height=400, width=700)
    p.line('date', 'temp', source=source, line_width=2, color="orange")

    # DateSlider pour filtrer
    slider = DateSlider(title="Choisir une date", start=dates[0], end=dates[-1], value=dates[0], step=1)

    # JS callback
    callback = CustomJS(args=dict(source=source, original=original, slider=slider), code="""
        const selectedDate = slider.value; // en millisecondes
        const full_data = original.data;
        const new_data = {date: [], temp: []};

        for (let i = 0; i < full_data['date_ms'].length; i++) {
            if (full_data['date_ms'][i] === selectedDate) {
                new_data['date'].push(full_data['date'][i]);
                new_data['temp'].push(full_data['temp'][i]);
            }
        }

        source.data = new_data;
        source.change.emit();
    """)
    slider.js_on_change('value', callback)

    layout = column(slider, p)
    return components(layout)
