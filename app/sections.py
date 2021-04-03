from typing import *

from pydantic import BaseModel, root_validator
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Br


class Section(BaseModel):
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

class LinearAlgebraSection(Section):
    title: str = "Linear Algebra"

    def section_header(
            self,
            attach_classes: str = None
    ) -> html.H3:
        if attach_classes is None:
            attach_classes = "section-header"
        return html.H3(self.title, className=attach_classes)

    @staticmethod
    def p_value_slider(
            id: str = "p-slider",
            min: int = -2,
            max: int = 10,
            value: int = 2,
            step: int = 1,
            marks: Dict[int, str] = None,
    ) -> dcc.Slider:
        if marks is None:
            marks = {
                -2: "-2 (min singular value)",
                1: "1 - L1 Norm",
                2: "2 - L2 Norm",
                10: "10"
            }

        slider = dcc.Slider(id=id, min=min, max=max, value=value, marks=marks, step=step)
        return slider

    def get_dash_layout(
            self,
    ) -> List:
        layout = [
            self.section_header(),
            html.Div(["Input a vector: ", dcc.Input(id='vector-input', value="(2, 2)", type='text')]),
            Br(),
            html.Div(["Input range of p: ", dcc.Input(id='p-range-input', value="(-2, 2)", type='text')]),
            Br(),
            html.Button(id='submit-button-state', n_clicks=0, children='Plot norms!'),
            Br(),
            Br(),
            self.graph("p-vs-norm-plot"),
            Br(),
            self.graph("p-isolines-plot")
        ]

        return layout