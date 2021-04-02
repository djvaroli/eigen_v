from typing import *
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go

from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from numpy import linalg

from sections import *
import data_utils

DEBUG = bool(int(os.environ.get("DEBUG", 1)))
PORT = os.environ.get("PORT", "8050")
HOST = os.environ.get("HOST", "127.0.0.1")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


section = LinearAlgebraSection()
layout = [
    section.section_header(),
    section.text_block(text="One topic that I come up against almost daily is Linear Algebra. That shouldn't be a surprise,"
                            " since so many things in machine learning and statistics (and other areas) are tightly connected to"
                            "linear algebra. Sometimes it feels overwhelming realizing, just how much you don't know. "
                            "I've decided that to strengthen my understanding (not just knowledge) of linear algebra concepts, "
                            "I will create small visualizations that will hopefully help me (and maybe others) get a more intuitive"
                            "understanding of some of these concepts that I struggle with. "),
    Br(),
    section.sub_section_header("Lp Norms"),
    Br(),
    Br(),
    html.Div(["Input a vector: ", dcc.Input(id='vector-input', value="(2, 2)", type='text')]),
    Br(),
    html.Div(["Input range of p: ", dcc.Input(id='p-range-input', value="(-2, 2)", type='text')]),
    Br(),
    html.Button(id='submit-button-state', n_clicks=0, children='Plot norms', className="fancy-button"),
    Br(),
    Br(),
    section.graph("p-vs-norm-plot"),
    Br(),
    section.text_block("After making these plots and playing around with the ranges of values of p I noticed some "
                       "interesting and unexpected observations.\n"
                       "The first thing that really stuck out was that as we increase p, in other words as p approaches"
                       " +inf the value of the Lp norm seems to converge to a finite number. What is even more interesting,"
                       "as I found out, is that if you play around with the values of the components of the input vector,"
                       "you will see that as p -> +inf the norm converges to the scalar equal to the largest component of "
                       "the input vector. As I found out this even has a name, the Chebyshev norm."),
    Br(),
    section.sub_section_header("Norm Iso-contours"),
    Br(),
    html.Div(["Input p: ", dcc.Input(id='p-isoline-input', value=2, type='number')]),
    Br(),
    html.Button(id='p-isoline-submit-button', n_clicks=0, children='Plot iso-contours', className="fancy-button"),
    Br(),
    Br(),
    section.graph("p-isolines-plot"),
    Br(),
    section.text_block("That looks so cool! I've seen such plots many times, but never quite understood how they are made."
                       "It actually wasn't that hard to recreate and I actually think I now better understand what the different"
                       "p norms 'look like' outside of their mathematical definition. ")
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

    fig = go.Figure(data=go.Scatter(x=x_data, y=y_data, line=dict(color="#e3506f")))
    fig.update_layout(
        title="Plot of p vs Lp Norm",
        xaxis_title="Value of p",
        yaxis_title="Lp Norm"
    )
    return fig


@app.callback(
    Output(component_id="p-isolines-plot", component_property="figure"),
    Input(component_id="p-isoline-submit-button", component_property="n_clicks"),
    State(component_id="p-isoline-input", component_property="value")
)
def p_isoline_plot(n_clicks, p):
    z_slices = [1.0, 3.0, 5.0]

    x = np.linspace(-5, 5, num=500)
    y = np.linspace(-5, 5, num=500)

    xx, yy = np.meshgrid(x, y)

    r = np.power(np.abs(xx), p) + np.power(np.abs(yy), p)

    fig = go.Figure()
    fig.add_trace(go.Contour(z=r, x=x, y=y, colorscale="sunsetdark"))

    fig.update_layout(
        title=f"Iso-lines for p = {p} in 2D.",
        xaxis_title=r"x_0",
        yaxis_title=r"x_1"
    )

    return fig


if __name__ == '__main__':
    print(f"DEBUG set to {DEBUG}")
    print(f"Running on HOST {HOST}")
    print(f"Running on port {PORT}")
    app.run_server(host=HOST, debug=DEBUG, port=PORT)
