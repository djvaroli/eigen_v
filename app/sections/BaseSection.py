from pydantic import BaseModel
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Br
import dash_bootstrap_components as dbc


class BaseSection(BaseModel):
    title: str
    name: str = None

    @staticmethod
    def graph(
            graph_id: str,
            attach_classes: str = ""
    ):
        attach_classes_list: list = attach_classes.strip().split(" ")
        attach_classes_list.append("fancy-plot")
        attach_classes = " ".join(attach_classes_list)
        return dcc.Graph(id=graph_id, className=attach_classes)

    def sub_section_header(
            self,
            sub_section_name: str,
            attach_classes: str = None
    ):
        if attach_classes is None:
            attach_classes = "sub-section-header"
        return html.H5(sub_section_name, className=attach_classes)

    def text_block(
            self,
            text: str,
            attach_classes: str = None
    ):
        if attach_classes is None:
            attach_classes = "fancy-text"

        return html.Div(text, className=attach_classes)

    @staticmethod
    def get_button(
            text: str,
            id: str,
            color: str = "light",
            attach_classes: str = ""
    ):
        attach_classes_list: list = attach_classes.strip().split(" ")
        attach_classes_list.append("fancy-button")
        attach_classes_list.append("btn")
        attach_classes_list.append("mr-1")
        attach_classes = " ".join(attach_classes_list)
        button = dbc.Button(text, id=id, color=color, className=attach_classes)

        return button

    @staticmethod
    def get_breaks(
            n: int = 1
    ):
        breaks = []
        for i in range(n):
            breaks.append(Br())
        return breaks