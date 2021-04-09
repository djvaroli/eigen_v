import dash_bootstrap_components as dbc

from components.BaseComponent import BaseComponent
from components import url_component_map


class NavBarComponent(BaseComponent):
    title = "Navigation Bar"

    def layout(
            self,
            current_section_url: str,
            make_dash_component: bool = True,
    ):
        current_section_blob = url_component_map.get(current_section_url)
        if current_section_blob is None:
            current_section_name = "404"
        else:
            current_section_name = current_section_blob.get("name")

        children = [
            dbc.DropdownMenuItem(section['name'], href=f"/{section_url}") for
            section_url, section in url_component_map.items() if section_url not in ["home", ""]
        ]

        label = current_section_name if current_section_name.lower() not in ["404", "home"] else "Select section..."
        layout = dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("", href="#")),
                dbc.DropdownMenu(
                    children=children,
                    nav=True,
                    in_navbar=True,
                    label=label,
                    className="navbar-dropdown"
                ),
            ],
            brand=f"EigenVo | {current_section_name}",
            brand_href="/home",
            color="info",
            dark=True,
        )

        return layout
