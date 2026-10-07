from nicegui import ui,app,context, Client

import plotly.graph_objects as go
#from niceplotly_resampler import FigureResampler
from plotly_resampler import FigureResampler, FigureWidgetResampler
from plotly.subplots import make_subplots
import plotly.express as px
from random import random

import pandas as pd

pos = 0
df = None
fig1 = None
plot = None
step = 10000

@ui.page('/plots')
async def plot_page(client: Client) -> None:
    with ui.header().classes('justify-center'):
        plots_label = ui.label(f'Nice Plots').classes('text-4xl font-bold')
    navigation = ui.row()
    with navigation:
        ui.link('Home', '/')
    ui.element('iframe').props('src="http://rubi.acs-lab.eonerc.rwth-aachen.de:8050"').classes('w-full h-[calc(100vh-3em)]')
    """
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


    fig = FigureResampler(make_subplots(rows=4, cols=1,shared_xaxes=True, vertical_spacing=0.01))


    fig.add_trace(
        go.Scattergl(
            name = "Integral",
            x = df.index ,
            y = df["i"].values,
            showlegend = True,
        )
    )
    fig.add_trace(
        go.Scattergl(
            name = "Proportional",
            x = df.index ,
            y = df["p"].values,
            showlegend = True,
        )
    )
    fig.add_trace(
        go.Scattergl(
            name = "Setpoint",
            x = df.index ,
            y = df["setpoint"].values,
            showlegend = True,
        )
    )
    fig.add_trace(
        go.Scattergl(
            name = "Phase",
            x = df.index ,
            y = df["phase"].values,
            showlegend = True,
        )
    )

    fig.update_layout(title='', title_x=0, margin= {'l': 0, 'r': 0, 't': 0, 'b': 0})#, height=1500)
    with ui.header().classes('justify-center'):
        plots_label = ui.label(f'Nice Plots').classes('text-4xl font-bold')

    navigation = ui.row()
    with navigation:
        ui.link('Home', '/')
    #with ui.row().classes('w-full h-full'):
    fig.show(options={"displayModeBar": False}).classes('w-full h-dvh')
    # Top: current value (centered)
    #with ui.header().classes('justify-center'):
    #    plots_label = ui.label(f'Nice Plots').classes('text-4xl font-bold')
    #plot = ui.plotly(fig1).classes('w-full h-dvh')

#    ui.plotly(fig2).classes('w-full h-60')

def update_datapoint():
    pass


app.timer(1,update_datapoint)


#fig = go.Figure()
#fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
#plot = ui.plotly(fig).classes('w-full h-40')

#def add_trace():
#    fig.add_trace(go.Scatter(x=[1, 2, 3], y=[random(), random(), random()]))
#    plot.update()

#ui.button('Add trace', on_click=add_trace)
"""