import numpy as np
from numpy import linalg
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import Lasso, Ridge
from sklearn import preprocessing

from app_factory import app
from utils import data_utils, math_utils
from assets.data.covid_data import COVID_DATA_DF


@app.callback(
    Output(component_id="p-vs-norm-plot", component_property="figure"),
    Input(component_id="p-vs-norm-vector-input", component_property="value"),
    Input(component_id="p-vs-norm-range-slider", component_property="value"),
)
def p_vs_norm_plot(vector_as_string: str, p_values: list):
    try:
        vector = data_utils.string_to_numpy(vector_as_string)
        p_values = list(range(p_values[0], p_values[-1]))

        if vector is None or p_values is None:
            x_data = [0]
            y_data = [0]
        else:
            norms = np.zeros(len(p_values))
            for i, p in enumerate(p_values):
                norms[i] = linalg.norm(vector, ord=p)
            x_data = p_values
            y_data = norms
    except Exception as e:
        raise PreventUpdate

    fig = go.Figure(data=go.Scatter(x=x_data, y=y_data, line=dict(color="#e3506f")))
    fig.update_layout(
        title="Plot of p vs Lp Norm",
        xaxis_title="Value of p",
        yaxis_title="Lp Norm"
    )
    return fig


@app.callback(
    Output(component_id="p-isolines-plot", component_property="figure"),
    Input(component_id="p-isoline-input", component_property="value")
)
def p_isoline_plot(p):
    if not p:
        raise PreventUpdate

    x = np.linspace(-5, 5, num=500)
    y = np.linspace(-5, 5, num=500)

    xx, yy = np.meshgrid(x, y)

    r = np.power(np.abs(xx), p) + np.power(np.abs(yy), p)

    fig = go.Figure()
    fig.add_trace(go.Contour(z=r, x=x, y=y, colorscale="PuRd"))

    fig.update_layout(
        title=f"Iso-lines for p = {p} in 2D.",
        xaxis_title=r"x_0",
        yaxis_title=r"x_1"
    )

    return fig


@app.callback(
    Output(component_id="covid-data-scatter", component_property="figure"),
    Input(component_id="covid-data-region-selector", component_property="value")
)
def covid_data_day_vs_region(region: str):
    title = f"March 2020 Covid cases by day in {region}"
    fig = px.scatter(COVID_DATA_DF, x="days", y=region, title=title)

    return fig

@app.callback(
    Output("covid-poly-fit-plot", "figure"),
    Input("covid-data-region-selector", "value"),
    Input("poly-degree-input", "value"),
    Input("alpha-range-slider", "value"),
    Input("kind-value-selector", "value")
)
def covid_data_poly_fit(region: str, degree: int, alphas, kind: str):
    if not isinstance(degree, int):
        raise PreventUpdate
    print(alphas)

    alphas = alphas.strip().split(",")
    alphas = [float(a) for a in alphas]

    # keep the untransformed values for future use
    x_raw = COVID_DATA_DF['days'].to_numpy().reshape(-1, 1)
    y_raw = COVID_DATA_DF[region].to_numpy()

    # standardize to have mean of 0 and std of 1
    st_scaler = preprocessing.StandardScaler()
    x = st_scaler.fit_transform(x_raw)
    y = y_raw.copy()
    # y = st_scaler.fit_transform(y_raw.reshape((-1, 1))).flatten()

    # transform features into n-degree polynomial space
    poly = preprocessing.PolynomialFeatures(degree, include_bias=False)
    x_poly = poly.fit_transform(x)

    # select which model to use
    model_selector = {
        "lasso": Lasso,
        "ridge": Ridge,
    }

    fig = make_subplots(
        rows=len(alphas) // 2,
        cols=2,
        shared_yaxes=True,
        subplot_titles=[f"alpha: {int(a)}" for a in alphas]
    )

    x_axis = x_raw.copy()
    x_axis_scaled = st_scaler.transform(x_axis)
    x_axis_poly = poly.transform(x_axis_scaled)

    row_column_permutations = math_utils.row_column_permutations(len(alphas) // 2, 2)
    for i, alpha in enumerate(alphas):
        row, col = row_column_permutations[i]
        model = model_selector.get(kind.lower())(alpha=alpha, max_iter=2000)
        model.fit(x_poly, y)
        predictions = model.predict(x_axis_poly)
        fig.add_trace(go.Scatter(x=np.round(x_axis, 2)[:, 0], y=predictions, mode="lines"), row=row, col=col)
        fig.add_trace(
            go.Scatter(
                x=x_raw.flatten(),
                y=y_raw.flatten(),
                mode="markers",
                marker={
                    "color": "#F57F53",
                    "size": 10
                },
                name="Actual cases"
            ),
            col=col,
            row=row
        )

    fig.update_layout(
        height=1200,
        title_text=f"Polynomial fitting with {kind} regression.",
        showlegend=False
    )

    return fig