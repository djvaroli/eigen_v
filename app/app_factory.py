import logging

import dash
import dash_bootstrap_components as dbc

logger = logging.getLogger("App-factory.py")
logger.setLevel(logging.INFO)


def get_app():
    application = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
    application_server = application.server
    application.config.suppress_callback_exceptions = True

    return application, application_server


app, server = get_app()



