from typing import *

import dash_core_components as dcc
import dash_html_components as html

from components.BaseComponent import BaseComponent
from assets.data.covid_data import COVID_DATA_DF
from app_factory import app

linear_algebra_intro_text = """One topic that I come up against almost daily is Linear Algebra. When I took my first 
linear algebra course I thought it was easy. Very soon after that I realized there was much more to linear algebra than 
what I knew. To this day I find this topic fascinating but so so challenging. In this section I will explore some 
concepts that I find most interesting, most challenging or both!"""


norm_intro_text = """So what is an Lp norm? Well, you are probably familiar with the L1 and L2 norms, also known as 
the Manhattan Distance and the Eucledian norm. The l1 norm is the sum of the components of a vector, where as the L2 norm 
is the Euclidian distance between two vectors. More formally an Lp norm is defined by the equation a bit below. Below that 
you will find a small interactive graph where you can see how p affects the norm of a vector (that you get to specify)!"""

norm_observation_text = """If you play around with the slider you will notice something I found very interesting. First, 
as the value of p increases the Lp norm approaches a seemingly finite number. This is not any random number, but 
the value of the largest component of the input vector. It was important enough to get its own name - Chebyshev Norm"""

norm_isocontours_intro = """Norm isocontours are something I couldn't really grasp conceptually at all, until I tried
making the plot that you see below. In essence, norm isocontours are lines along which the norm of a vector, made up of 
the x and y - coordinates of the point on the contour is the same, regardless of which point on the contour you pick. 
Try a bunch of different values below and see how the isocontours change!"""

isocontours_text = """Pretty cool, huh? At least I think so. In any case one thing you may have already guessed is that 
since we are looking at a 2D vector in this example, the isocontours are just slices of some shape in 3D along a fixed 
value of z (if we assume x, y to be the components of the vector). Keep note of this as it will be important when we look 
at the applications in regularization."""

regularization_intro_text = """While all of this is very cool to look at on its own, we don't have to limit ourselves
to just some nice plots and shapes. Norms play an important role in machine learning when it comes to obtaining models
that generalize better and don't overfit the training data. This is called regularization and it is done by adding 
a penalty term equal to the some p-norm (usually 1 or 2) of the weights of our parameter vector. The cases where we use 
 the L1 and L2 norms are also called Lasso and Ridge regression respectively. Let's explore how those two 
 impact performance of a machine learning model. For this exercise I will go with the COVID cases data 
 (because that's the hot topic now) provided in the book."""

regularization_post_covid_scatter_text = """Looking at the scatter plots, we see that cases are not going up in a linear
fashion, so we will transform our features into some polynomial space and then fit our regression model to those 
transformed features to approximate the non-linear relationship. I just want to note that this is really done for 
as a demonstration you probably would do something very different if you were trying to make any predictions.\n 
The plot below will let you try out different degrees of the polynomial transformations as well as chose between the two 
regularization methods"""


class LinearAlgebraComponent(BaseComponent):
    title: str = "Linear Algebra"

    @staticmethod
    def p_value_range_slider(
            id: str,
            min: int = -5,
            max: int = 20,
            value: List[int] = None,
            step: int = 1,
            marks: Dict[int, str] = None,
            tooltip: Dict = None,
            *args,
            **kwargs
    ) -> dcc.RangeSlider:
        if marks is None:
            marks = {
                2: "p = 2",
                10: "p = 10"
            }
            # marks = {val: f"p = {val}" for val in range(min, max + 1, step)}

        if value is None:
            value = [2, 10]

        if tooltip is None:
            tooltip = {
                "placement": "right"
            }

        slider = dcc.RangeSlider(
            id=id,
            min=min,
            max=max,
            value=value,
            marks=marks,
            step=step,
            tooltip=tooltip,
            *args,
            **kwargs
        )
        return slider

    @staticmethod
    def alpha_value_range_slider(
            id: str,
            min: int = 0,
            max: int = 5000,
            value: List[int] = None,
            step: Optional[Union[int, None]] = None,
            marks: Dict[int, str] = None,
            tooltip: Dict = None,
            *args,
            **kwargs
    ) -> dcc.RangeSlider:
        if marks is None:
            marks = {
                0: "0",
                10: "10",
                100: "100",
                1000: "alpha = 1000",
                10000: "alpha = 5"
            }

        if value is None:
            value = [0, 100]

        if tooltip is None:
            tooltip = {
                "placement": "right"
            }

        slider = dcc.RangeSlider(
            id=id,
            min=min,
            max=max,
            value=value,
            marks=marks,
            step=step,
            tooltip=tooltip,
            *args,
            **kwargs
        )
        return slider

    def vector_input_form_group(
            self,
            id: str,
            type: str = "text",
            input_width: int = 4,
            row: bool = True,
            placeholder: str = "2D Vector goes here. Try (2,2)",
            *args,
            **kwargs
    ):
        return self.input_form_group(
            id=id,
            type=type,
            input_width=input_width,
            row=row,
            placeholder=placeholder,
            *args,
            **kwargs
        )

    def isoline_plot_p_form_group(
            self,
            id: str,
            type: str = "number",
            input_width: int = 4,
            row: bool = True,
            placeholder: str = "Enter a value of P",
            *args,
            **kwargs
    ):
        return self.input_form_group(
            id=id,
            type=type,
            input_width=input_width,
            row=row,
            placeholder=placeholder,
            *args,
            **kwargs
        )

    def covid_data_region_select(
            self,
            id: str,
            classes_to_attach: List[str] = None,
            *args,
            **kwargs
    ):
        regions = COVID_DATA_DF.columns.to_list()
        regions = [r for r in regions if r.lower() not in ['days', 'date']]
        options = [{"label": r, "value": r} for r in regions]
        return self.dropdown_select(
            id, options=options, value="Ile-de-France", classes_to_attach=classes_to_attach, *args, **kwargs
        )

    def get_regression_type_selector(
            self,
            id: str,
            classes_to_attach: List[str] = None,
            *args,
            **kwargs
    ):
        labels = ['Lasso regression', "Ridge regression"]
        values = ["lasso", "ridge"]

        options = [{"label": r[0], "value": r[-1]} for r in zip(labels, values)]
        return self.dropdown_select(
            id,
            value="lasso",
            options=options,
            classes_to_attach=classes_to_attach,
            *args,
            **kwargs
        )

    def get_polynomial_degree_input(
            self,
            id: str,
            type: str = "number",
            input_width: int = 4,
            row: bool = True,
            placeholder: str = "Degree of Polynomial Features",
            *args,
            **kwargs
    ):
        return self.input_form_group(
            id=id,
            type=type,
            input_width=input_width,
            row=row,
            step=1,
            placeholder=placeholder,
            *args,
            **kwargs
        )

    def layout(
            self,
            make_dash_component: bool = False,
            *args,
            **kwargs
    ):
        layout = [
            *self.text_block(text=linear_algebra_intro_text),
            *self.sub_section_header("Lp Norms"),
            *self.text_block(norm_intro_text),
            *self.image(app.get_asset_url("images/lp_norm_equation.png")),
            *self.vector_input_form_group("p-vs-norm-vector-input"),
            self.p_value_range_slider("p-vs-norm-range-slider"),
            *self.figure("p-vs-norm-plot"),
            *self.text_block(norm_observation_text),
            *self.sub_section_header("Norm Iso-contours"),
            *self.text_block(norm_isocontours_intro),
            *self.isoline_plot_p_form_group('p-isoline-input'),
            *self.figure("p-isolines-plot"),
            *self.text_block(isocontours_text),
            *self.sub_section_header("Application in Regularization"),
            *self.text_block(regularization_intro_text),
            *self.text_block(regularization_post_covid_scatter_text),
            *self.figure("covid-data-scatter"),
            *self.covid_data_region_select("covid-data-region-selector"),
            *self.get_regression_type_selector("kind-value-selector"),
            *self.get_polynomial_degree_input("poly-degree-input"),
            *self.figure("covid-poly-fit-plot")
        ]

        if make_dash_component:
            layout = html.Div(layout, className="container")

        return layout
