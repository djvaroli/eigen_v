import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from numpy import linalg


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.H3("Lp Norms.", className="section-header"),
    html.Div(["Input: ",
              dcc.Input(id='vector-input', value='[1, 2]', type='text')]),
    html.Br(),
    html.H6("Select a value of p"),
    dcc.Slider(
        id='p-slider',
        min=-2,
        max=10,
        value=2,
        marks={
            -2: "-2 (min singular value)",
            1: "1 - L1 Norm",
            2: "2 - L2 Norm",
            10: "10"
        },
        step=1
    ),
    html.Div(id="selected-p-value"),
    html.Div(id='norm-output'),
])


@app.callback(
    Output(component_id='norm-output', component_property='children'),
    Output(component_id='selected-p-value', component_property='children'),
    Input(component_id='vector-input', component_property='value'),
    Input(component_id='p-slider', component_property='value')
)
def update_output_div(vector_string, p):
    
    vector = vector_string.replace("[", "").replace("]", "").strip()
    vector = vector.split(",")
    vector = np.array(vector).astype(np.int32)
    norm = linalg.norm(vector, ord=p)
    return f"L2 Norm: {norm: .4f}", f"p: {p}"

if __name__ == '__main__':
    app.run_server(debug=True)
