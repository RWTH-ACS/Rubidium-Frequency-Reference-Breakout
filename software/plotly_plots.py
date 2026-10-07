import plotly.graph_objects as go; import numpy as np
from plotly_resampler import FigureResampler, FigureWidgetResampler
from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback, State


app = Dash(__name__)
app.layout = html.Div([
    html.Button("Start/Stop Update", id='start-stop-button'),
    html.Div([
        html.H4('Rubidium Setpoint History'),
        dcc.Graph(id='live-update-graph', style={'height': '2000px'}),
        dcc.Interval(
            id='interval-component',
            interval=30*1000, # in milliseconds
            n_intervals=0
        )
    ])]
)

@app.callback(
    Output('interval-component', 'disabled'),
    [Input('start-stop-button', 'n_clicks')],
    [State('interval-component', 'disabled')],
)
def callback_func_start_stop_interval(button_clicks, disabled_state):
    if button_clicks is not None and button_clicks > 0:
        return not disabled_state
    else:
        return disabled_state

# Multiple components can update everytime interval gets fired.
@callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    # df = pd.read_csv("data/2025-12-17_18_05_18.csv")
    # df.columns=["time", "phase", "setpoint", "p", "i","register", "room_temp", "device_temp", "phase2", "phase3"]

    # df['datetime'] = pd.to_datetime(df['time'], unit='s')
    # #df.datetime = df.datetime.dt.tz_localize('UTC').dt.tz_convert("Europe/Berlin")
    # df.datetime= df.datetime + pd.DateOffset(hours=1)
    # df.set_index("datetime", inplace=True)
    # df.drop(df.head(23000).index,inplace=True)


    # df_1 = pd.read_csv("data/2025-12-27_08_11_22.csv")
    # df_1.columns=["time", "phase", "setpoint", "p", "i","register", "room_temp", "device_temp", "phase2", "phase3"]

    # df_1['datetime'] = pd.to_datetime(df_1['time'], unit='s')
    # #df.datetime = df.datetime.dt.tz_localize('UTC').dt.tz_convert("Europe/Berlin")
    # df_1.datetime= df_1.datetime + pd.DateOffset(hours=1)
    # df_1.set_index("datetime", inplace=True)
    # df_1.drop(df_1.head(1000).index,inplace=True)

    # #df = pd.concat([df_0, df_1], ignore_index=True)


    # df = pd.concat([df, df_1],axis=0)


    df = pd.read_csv("data/2026-01-18_15_00_07.csv")
    df.columns=["time", "phase", "setpoint", "p", "i","register", "room_temp", "device_temp", "phase2", "phase3"]

    df['datetime'] = pd.to_datetime(df['time'], unit='s')
    #df.datetime = df.datetime.dt.tz_localize('UTC').dt.tz_convert("Europe/Berlin")
    df.datetime= df.datetime + pd.DateOffset(hours=1)
    df.set_index("datetime", inplace=True)
    #df.drop(df.head(23000).index,inplace=True)

    
    #dfs = list()
    #for f in files:
    #    d = pd.read_csv(f, index_col=None)
    #    dfs.append(d)
        
    #df = pd.concat(dfs, ignore_index=True)
    


    # df['datetime'] = pd.to_datetime(df['time'], unit='s')
    # #df.datetime = df.datetime.dt.tz_localize('UTC').dt.tz_convert("Europe/Berlin")
    # df.datetime= df.datetime + pd.DateOffset(hours=1)
    # df.set_index("datetime", inplace=True)

    fig = FigureResampler(make_subplots(rows=7, cols=1,shared_xaxes=True, vertical_spacing=0.01))


    fig.add_trace(
        go.Scattergl(
            name = "Integral",
    #        x = df["time"].values ,
    #        y = df["i"].values,
            showlegend = True,
            #y="Integral [Hz]"
        ),
        hf_x = df.index,
        hf_y = df["i"].values,
        row = 1,
        col = 1
    )

    fig.add_trace(
        go.Scattergl(
            name = "Proportional",
            showlegend = True,
            #y="Proportional [Hz]"
        ),
        hf_x = df.index,
        hf_y = df["p"].values,
        row = 2,
        col = 1
    )
    fig.add_trace(
        go.Scattergl(
            name = "Setpoint",
            showlegend = True,
            #y="Setpoint [Hz]"
        ),
        hf_x = df.index,
        hf_y = df["setpoint"].values,
        row = 3,
        col = 1
    )
    fig.add_trace(
        go.Scattergl(
            name = "Phase",
            showlegend = True,
            #y="Phase [Deg]"
        ),
        hf_x = df.index,
        hf_y = df["phase"].values,
        row = 4,
        col = 1
    )

    fig.add_trace(
        go.Scattergl(
            name = "Room_Temp",
            showlegend = True,
            #y="Temperature [Degree]"
        ),
        hf_x = df.index,
        hf_y = df["room_temp"].values,
        row = 5,
        col = 1
    )

    fig.add_trace(
        go.Scattergl(
            name = "Device_Temp",
            showlegend = True,
            #y="Temperature [Degree]"
        ),
        hf_x = df.index,
        hf_y = df["device_temp"].values,
        row = 6,
        col = 1
    )
    fig.add_trace(
        go.Scattergl(
            name = "Phase Buffered 10 MHz 1",
            showlegend = True,
            #y="Phase [Deg]"

        ),
        hf_x = df.index,
        hf_y = df["phase2"].values,
        row = 7,
        col = 1
    )
    fig.add_trace(
        go.Scattergl(
            name = "Phase Buffered 10 MHz 2",
            showlegend = True,
        ),
        hf_x = df.index,
        hf_y = df["phase3"].values,
        row = 7,
        col = 1
    )

    dow = df.index.to_series().dt.dayofweek
    change_mask = dow.ne(dow.shift())
    change_idx = df.index[change_mask]
    change_idx = change_idx.append(df.index[-1:])
    s = None
    c = 1
    for e in change_idx:
        if s is None:
            s = e
            continue
        if c%2 == 0:
            fig.add_vrect(
                x0=s.round('s'), x1=e.round('s'),
                fillcolor="LightSalmon", opacity=0.2,
                layer="below", line_width=0,
            )
        s = e
        c += 1



    fig.update_layout(title='', title_x=0, margin= {'l': 0, 'r': 0, 't': 0, 'b': 0})#, height=1500)

    #fig.show_dash(mode='inline',debug=False, host='0.0.0.0')
    return fig

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")