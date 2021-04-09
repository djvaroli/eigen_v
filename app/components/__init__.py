import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from components import LinearAlgebraComponent
from components.BaseComponent import BaseComponent


url_component_map = {
    "linear_algebra": {
        "component": LinearAlgebraComponent.LinearAlgebraComponent(),
        "name": "Linear Algebra",
        "description": "Linear Algebra"
    }
}


# special case where we need the home component in the map but
# following the patter for other components means creating a circular import
class HomeComponent(BaseComponent):
    title = "Home"

    def layout(
            self,
            make_dash_component: bool = None,
            *args,
            **kwargs
    ):
        return html.Div(html.H1("Eigenvo - the Math Playground."), className="container")


url_component_map.update({
    "home": {
        "component": HomeComponent(),
        "name": "Home"
    }
})

