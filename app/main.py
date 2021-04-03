import logging
import os

import numpy as np
from numpy import linalg
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import dash_html_components as html

from utils import data_utils
from sections.LinearAlgebraSection import LinearAlgebraSection
from app_factory import get_app

ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")
PORT = os.environ.get("PORT", "8050")
HOST = os.environ.get("HOST", "0.0.0.0")

logger = logging.getLogger("eigenvo-main.py")
logger.setLevel(logging.INFO)

section = LinearAlgebraSection()
layout = section.build_layout()

app, server = get_app()
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
    debug = True
    if ENVIRONMENT == "production":
        debug = False

    logger.info(f"Running in {ENVIRONMENT}")
    logger.info(f"Running on host {HOST} @ port {PORT}, ")
    app.run_server(host=HOST, debug=debug, port=PORT)