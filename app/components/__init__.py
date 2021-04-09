import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from components import LinearAlgebraComponent
from components.BaseComponent import BaseComponent


url_component_map = {
    "linear_algebra": {
        "component": LinearAlgebraComponent.LinearAlgebraComponent(),
        "name": "Linear Algebra",
        "description": "Vectors, matrices, norms, eigenvalues and eigenvectors and much much more. (With applications!)",
        "logo_path": "/assets/images/matrix.png"
    }
}


# special case where we need the home component in the map but
# following the patter for other components means creating a circular import
class HomeComponent(BaseComponent):
    title = "Home"

    def make_section_entry(
            self,
            section_url,
            section_blob
    ):
        link = html.A(section_blob['name'], href=f"/{section_url}", className="home-section-link")
        description = html.P(section_blob['description'], className="home-section-description")
        # image = html.Img(src=section_blob['logo_path'])
        return html.Div([link, description])

    def layout(
            self,
            make_dash_component: bool = None,
            *args,
            **kwargs
    ):
        headers = html.Div([html.H1("EigenVo - the Math Playground.", className="home-header mt-4 mb-4")])

        sections =html.Div([
            html.H3("Sections currently live", className="home-subheader mb-3"),
            *[
                self.make_section_entry(section_url, section) for section_url, section in url_component_map.items()
                if section_url not in ["home", ""]
            ]
        ], className="home-live-sections")
        return html.Div([headers, sections], className="container")


url_component_map.update({
    "home": {
        "component": HomeComponent(),
        "name": "Home"
    },
    "": {
        "component": HomeComponent(),
        "name": "Home"
    },
})

