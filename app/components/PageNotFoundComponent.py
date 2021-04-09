from typing import *

import dash_html_components as html

from components.BaseComponent import BaseComponent
from utils import decorators


class PageNotFoundComponent(BaseComponent):
    title = "Page Not Found (404... Sorry!)"
    icon_url: str = "/assets/images/404.png"

    @decorators.use_default_classes("center m-5")
    def layout(
            self,
            make_dash_component: bool = True,
            classes_to_attach: List[str] = None,
            *args,
            **kwargs
    ):
        default_classes = kwargs.pop("default_classes", [])
        classes_to_attach = self.make_classes(classes_to_attach, default_classes)
        layout = [
            html.H1(self.title),
            html.Img(src=self.icon_url)
        ]
        if make_dash_component:
            layout = html.Div(layout, className=classes_to_attach)

        return layout
