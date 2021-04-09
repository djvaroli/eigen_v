import logging
import os

import dash
import dash_core_components as dcc
import dash_html_components as html

from app_factory import app
from components import PageNotFoundComponent, NavBarComponent
from components import url_component_map
from callbacks import linear_algebra_callbacks


logger = logging.getLogger("eigenvo-main.py")
logger.setLevel(logging.INFO)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def router(pathname):
    pathname = pathname.replace("/", "")
    navbar = NavBarComponent.NavBarComponent().layout(pathname)
    component = url_component_map.get(pathname, None)
    if component is None:
        component = PageNotFoundComponent.PageNotFoundComponent()
    else:
        component = component['component']

    layout = html.Div([navbar, component.layout(make_dash_component=True)])
    return layout


if __name__ == '__main__':
    debug = True
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")
    PORT = os.environ.get("PORT", "8050")
    HOST = os.environ.get("HOST", "0.0.0.0")

    if ENVIRONMENT == "production":
        debug = False

    logger.info(f"Running in {ENVIRONMENT}")
    logger.info(f"Running on host {HOST} @ port {PORT}, ")
    app.run_server(host=HOST, debug=debug, port=PORT)