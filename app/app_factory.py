import os
import logging

import dash
import dash_bootstrap_components as dbc

logger = logging.getLogger("App-factory.py")
logger.setLevel(logging.INFO)


def get_app():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    server = app.server
    app.config.suppress_callback_exceptions = True

    return app, server



