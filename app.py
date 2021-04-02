from typing import *
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Br
import plotly.express as px
import plotly.graph_objects as go

from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from numpy import linalg

from sections import *
import data_utils

DEBUG = bool(int(os.environ.get("DEBUG", 0)))
PORT = os.environ.get("PORT", "8050")
HOST = os.environ.get("HOST", "127.0.0.1")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


section = LpNormSection()


layout = [
    section.section_header(),
    html.Div(["Input a vector: ", dcc.Input(id='vector-input', value="(2, 2)", type='text')]),
    Br(),
    html.Div(["Input range of p: ", dcc.Input(id='p-range-input', value="(-2, 2)", type='text')]),
    Br(),
    html.Button(id='submit-button-state', n_clicks=0, children='Plot norms!'),
    Br(),
    Br(),
    section.graph("p-vs-norm-plot"),
]

app.layout = html.Div(layout, className="container")


@app.callback(
    Output(component_id="p-vs-norm-plot", component_property="figure"),
    Input(component_id="submit-button-state", component_property="n_clicks"),
    State(component_id="vector-input", component_property="value"),
    State(component_id="p-range-input", component_property="value"),
)
def p_vs_norm_plot(n_clicks, vector_as_string: str, p_range_as_string: str):
    vector = data_utils.string_to_numpy(vector_as_string)
    p_values = data_utils.string_to_range(p_range_as_string, return_list=True)

    if vector is None or p_values is None:
        x_data = [0]
        y_data = [0]
    else:
        norms = np.zeros(len(p_values))
        for i, p in enumerate(p_values):
            norms[i] = linalg.norm(vector, ord=p)
        x_data = p_values
        y_data = norms

    fig = go.Figure(data=go.Scatter(x=x_data, y=y_data))
    fig.update_layout(
        title="Plot of p vs Lp Norm",
        xaxis_title="Value of p",
        yaxis_title="Lp Norm"
    )
    return fig


if __name__ == '__main__':
    print(f"DEBUG set to {DEBUG}")
    print(f"Running on HOST {HOST}")
    print(f"Running on port {PORT}")
    app.run_server(host=HOST, debug=DEBUG, port=PORT)
