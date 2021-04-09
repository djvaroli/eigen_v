import dash_bootstrap_components as dbc

from components.BaseComponent import BaseComponent
from components import LinearAlgebraComponent, HomeComponent

url_section_map = {
    "linear_algebra": {
        "component": LinearAlgebraComponent.LinearAlgebraComponent(),
        "name": "Linear Algebra"
    },
    "home": {
        "component": HomeComponent.HomeComponent(),
        "name": "Home"
    }
}


class NavBarComponent(BaseComponent):
    title = "Navigation Bar"

    def layout(
            self,
            current_section_url: str,
            make_dash_component: bool = True,
    ):
        current_section_blob = url_section_map.get(current_section_url)
        if current_section_blob is None:
            current_section_name = "Select a section"
        else:
            current_section_name = current_section_blob.get("name")

        children = [
            dbc.DropdownMenuItem(section['name'], href=f"/{section_url}") for
            section_url, section in url_section_map.items()
        ]

        layout = dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("", href="#")),
                dbc.DropdownMenu(
                    children=children,
                    nav=True,
                    in_navbar=True,
                    label=current_section_name,
                    className="navbar-dropdown"
                ),
            ],
            brand=f"EigenVo | {current_section_name}",
            brand_href="/home",
            color="info",
            dark=True,
        )

        return layout
