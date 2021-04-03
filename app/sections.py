from typing import *

from pydantic import BaseModel, root_validator
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Br
import dash_bootstrap_components as dbc

linear_algebra_intro_text = """One topic that I come up against almost daily is Linear Algebra. That shouldn't be a surprise,"
" since so many things in machine learning and statistics (and other areas) are tightly connected to"
"linear algebra. Sometimes it feels overwhelming realizing, just how much you don't know. "
"I've decided that to strengthen my understanding (not just knowledge) of linear algebra concepts, "
"I will create small visualizations that will hopefully help me (and maybe others) get a more intuitive"
"understanding of some of these concepts that I struggle with."""

norm_observation_text = """After making these plots and playing around with the ranges of values of p I noticed some "
"interesting and unexpected observations.\n"
"The first thing that really stuck out was that as we increase p, in other words as p approaches"
" +inf the value of the Lp norm seems to converge to a finite number. What is even more interesting,"
"as I found out, is that if you play around with the values of the components of the input vector,"
"you will see that as p -> +inf the norm converges to the scalar equal to the largest component of "
"the input vector. As I found out this even has a name, the Chebyshev norm."""

isocontours_text = """That looks so cool! I've seen such plots many times, but never quite understood how they are made."
"It actually wasn't that hard to recreate and I actually think I now better understand what the different"
"p norms 'look like' outside of their mathematical definition. """


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

    def get_button(
            self,
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

    @staticmethod
    def get_vector_input_form(
            label_width: int = 2,
            input_width: int = 2,
            row: bool = True,
            initial_value: str = "(2, 2)"
    ):
        f = dbc.FormGroup(
            [
                dbc.Label("Input vector", width=label_width),
                dbc.Col(
                    dbc.Input(id="vector-input", type="text", value=initial_value),
                    width=input_width
                )
            ],
            row=row
        )

        return f

    @staticmethod
    def get_p_range_form(
            label_width: int = 2,
            input_width: int = 2,
            row: bool = True,
            initial_value: str = "(-2, 2)"
    ):
        f = dbc.FormGroup(
            [
                dbc.Label("Input p range", width=label_width),
                dbc.Col(
                    dbc.Input(id="p-range-input", type="text", value=initial_value),
                    width=input_width
                )
            ],
            row=row
        )
        return f

    @staticmethod
    def get_input_form_group(
            id: str,
            label_text: str,
            type: str,
            initial_value,
            row: bool = True,
            label_width: int = 2,
            input_width: int = 2,
    ):
        f = dbc.FormGroup(
            [
                dbc.Label(label_text, width=label_width),
                dbc.Col(
                    dbc.Input(id=id, type=type, value=initial_value),
                    width=input_width
                )
            ],
            row=row
        )

        return f


    def build_layout(
            self
    ):
        layout = [
            self.section_header(),
            *self.get_breaks(1),
            self.text_block(text=linear_algebra_intro_text),
            *self.get_breaks(1),
            self.sub_section_header("Lp Norms"),
            *self.get_breaks(),
            self.get_vector_input_form(),
            self.get_p_range_form(),
            self.get_button("Plot norms", id='submit-button-state'),
            *self.get_breaks(2),
            self.graph("p-vs-norm-plot"),
            *self.get_breaks(1),
            self.text_block(norm_observation_text),
            *self.get_breaks(1),
            self.sub_section_header("Norm Iso-contours"),
            *self.get_breaks(1),
            self.get_input_form_group('p-isoline-input', "Input p", "number", initial_value=2),
            *self.get_breaks(1),
            self.get_button('Plot iso-contours', id='p-isoline-submit-button'),
            *self.get_breaks(2),
            self.graph("p-isolines-plot"),
            *self.get_breaks(1),
            self.text_block(isocontours_text),
            *self.get_breaks(2)
        ]

        return layout
