from nicegui import ui,app,context, Client

import plotly.graph_objects as go

from random import random

import pandas as pd

pos = 0
df = None
fig1 = None
plot = None
step = 10000

@ui.page('/plots')
async def plot_page(client: Client) -> None:
    global fig1, df, plot
    df = pd.read_csv("./overnight.csv", skiprows=10000)
    df.columns=["time", "phase", "setpoint", "p", "i","register"]

    df['datetime'] = pd.to_datetime(df['time'], unit='s')
    #df.datetime = df.datetime.dt.tz_localize('UTC').dt.tz_convert("Europe/Berlin")
    df.datetime= df.datetime + pd.Timedelta('01:00:00')
    df.set_index("datetime", inplace=True)

    ##Remove recableing
    l = df.loc[(df.index > pd.to_datetime('2025-12-08 15:14:39')) & (df.index < pd.to_datetime('2025-12-08 15:14:42'))]
    df.drop(l.index, inplace=True)
    ##Update cabling and add active cooling. Afterwards about 10 deg cooler
    l = df.loc[(df.index > pd.to_datetime('2025-12-08 15:16:32')) & (df.index < pd.to_datetime('2025-12-08 15:16:35'))]
    df.drop(l.index, inplace=True)

    fig1 = {
        "data" : [
            {
                "type" : "scatter",
                "name" : "Integral",
                "x" : df["time"].values[:0],
                "y" : df["i"].values[:0]
            },
            {
                "type" : "scatter",
                "name" : "Proportional",
                "x" : df["time"].values[:0],
                "y" : df["p"].values[:0],
                "xaxis": 'x2',
                "yaxis": 'y2',
            },
            {
                "type" : "scatter",
                "name" : "Setpoint",
                "x" : df["time"].values[:0],
                "y" : df["setpoint"].values[:0],
                "xaxis": 'x3',
                "yaxis": 'y3',
            },
            {
                "type" : "scatter",
                "name" : "Phase",
                "x" : df["time"].values[:0],
                "y" : df["phase"].values[:0],
                "xaxis": 'x4',
                "yaxis": 'y4',
            },
        ],
        'layout': {
            "title" : "Integral",
            'margin': {'l': 15, 'r': 0, 't': 0, 'b': 15},
            'plot_bgcolor': '#E5ECF6',
            'xaxis': {'gridcolor': 'white', "title" : "Time"},
            "xaxis2" : {"matches" :'x'},
            "xaxis3" : {"matches" :'x'},
            "xaxis4" : {"matches" :'x'},
            'yaxis': {'gridcolor': 'white', "title" : "Integral"},
            "grid" : {"rows" : 4, "columns" : 1, "pattern" : "independent"},
        },
    }

    # Top: current value (centered)
    with ui.header().classes('justify-center'):
        plots_label = ui.label(f'Nice Plots').classes('text-4xl font-bold')
    plot = ui.plotly(fig1).classes('w-full h-dvh')

#    ui.plotly(fig2).classes('w-full h-60')
@ui.page('/test')
async def plot_page() -> None:
    ui.label("LOL")


def add_datapoint():
    global fig1, pos, plot, step
    if fig1 is None:
        return


    if step*pos < len(df["i"]):
        fig1["data"][0]["x"] = df["time"].values[:step*pos]
        fig1["data"][0]["y"] = df["i"].values[:step*pos]
        fig1["data"][1]["x"] = df["time"].values[:step*pos]
        fig1["data"][1]["y"] = df["p"].values[:step*pos]
        fig1["data"][2]["x"] = df["time"].values[:step*pos]
        fig1["data"][2]["y"] = df["setpoint"].values[:step*pos]
        fig1["data"][3]["x"] = df["time"].values[:step*pos]
        fig1["data"][3]["y"] = df["phase"].values[:step*pos]
        pos += 1
        plot.update_figure(fig1)


app.timer(0.1,add_datapoint)

#fig = go.Figure()
#fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
#plot = ui.plotly(fig).classes('w-full h-40')

#def add_trace():
#    fig.add_trace(go.Scatter(x=[1, 2, 3], y=[random(), random(), random()]))
#    plot.update()

#ui.button('Add trace', on_click=add_trace)
