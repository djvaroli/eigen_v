from typing import *

from pydantic import BaseModel
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from utils import convenience_functions, decorators


class BaseComponent(BaseModel):
    title: str
    name: str = None

    @staticmethod
    def make_classes(
            class_list: Union[List[str], str, None],
            additional_classes: Optional[Union[List[str], str]] = None
    ) -> str:
        if additional_classes is None:
            additional_classes = []

        if class_list is None:
            class_list = []

        if not isinstance(additional_classes, list):
            additional_classes = [additional_classes]

        if not isinstance(class_list, list):
            class_list = [class_list]

        classes = [*class_list, *additional_classes]
        return convenience_functions.list_to_string(classes, " ")

    @decorators.use_default_classes(default_classes="fancy-plot")
    @decorators.wrap_component_with_breaks()
    def figure(
            self,
            graph_id: str,
            classes_to_attach: List[str] = None,
            *args,
            **kwargs
    ):
        default_classes = kwargs.pop("default_classes", [])
        classes_to_attach = self.make_classes(classes_to_attach, default_classes)
        return dcc.Graph(id=graph_id, className=classes_to_attach, *args, **kwargs)

    @decorators.use_default_classes(default_classes="fancy-image")
    @decorators.wrap_component_with_breaks()
    def image(
            self,
            image_url: str,
            classes_to_attach: List[str] = None,
            *args,
            **kwargs
    ):
        default_classes = kwargs.pop("default_classes", [])
        classes_to_attach = self.make_classes(classes_to_attach, default_classes)
        return html.Img(src=image_url, className=classes_to_attach)

    @decorators.use_default_classes(default_classes="section-header")
    @decorators.wrap_component_with_breaks()
    def section_header(
            self,
            body: str,
            size: str = "H3",
            classes_to_attach: List[str] = None,
            *args,
            **kwargs
    ) -> html.Header:
        default_classes = kwargs.pop("default_classes", [])
        classes_to_attach = self.make_classes(classes_to_attach, default_classes)
        header = getattr(html, size.capitalize())
        component = header(body, className=classes_to_attach, *args, **kwargs)
        return component

    @decorators.use_default_classes(default_classes="sub-section-header")
    @decorators.wrap_component_with_breaks(1, 1)
    def sub_section_header(
            self,
            sub_section_name: str,
            size: str = "H5",
            classes_to_attach: List[str] = None,
            *args,
            **kwargs
    ):
        default_classes = kwargs.pop("default_classes", [])
        classes_to_attach = self.make_classes(classes_to_attach, default_classes)
        header = getattr(html, size.capitalize())
        component = header(sub_section_name, className=classes_to_attach, *args, **kwargs)
        return component

    @decorators.use_default_classes(default_classes="fancy-text")
    @decorators.wrap_component_with_breaks()
    def text_block(
            self,
            text: str,
            classes_to_attach: List[str] = None,
            wrap_in_tab: bool = False,
            tab_label: str = None,
            *args,
            **kwargs
    ):
        default_classes = kwargs.pop("default_classes", [])
        classes_to_attach = self.make_classes(classes_to_attach, default_classes)
        component = html.Div(text, className=classes_to_attach, *args, **kwargs)
        if wrap_in_tab:
            component = dbc.Tabs([
                dbc.Tab(component, label=tab_label)
            ])

        return component

    @decorators.use_default_classes(default_classes="fancy-button btn")
    @decorators.wrap_component_with_breaks()
    def button(
            self,
            text: str,
            id: str,
            color: str = "light",
            classes_to_attach: List[str] = None,
            *args,
            **kwargs
    ) -> dbc.Button:
        default_classes = kwargs.pop("default_classes", [])
        classes_to_attach = self.make_classes(classes_to_attach, default_classes)
        component = dbc.Button(text, id=id, color=color, className=classes_to_attach, *args, **kwargs)
        return component

    @decorators.wrap_component_with_breaks()
    def input_component(
            self,
            id: str,
            type: str,
            value: Any,
            label: Optional[str] = None,
            classes_to_attach: List[str] = None,
            *args,
            **kwargs
    ):
        classes_to_attach = self.make_classes(classes_to_attach)
        component = dbc.Input(
            id=id,
            className=classes_to_attach,
            type=type,
            value=value,
            *args,
            **kwargs
        )

        if label is not None:
            component = html.Div([
                html.P(label),
                component
            ])

        return component

    @staticmethod
    @decorators.wrap_component_with_breaks()
    def input_form_group(
            id: str,
            type: str,
            label_text: str = None,
            initial_value = None,
            row: bool = True,
            label_width: int = 2,
            input_width: int = 2,
            *args,
            **kwargs
    ):
        if label_text is None:
            label_ = []
        else:
            label_ = [dbc.Label(label_text, width=label_width)]

        f = dbc.FormGroup(
            [
                *label_,
                dbc.Col(
                    dbc.Input(
                        id=id,
                        type=type,
                        value=initial_value,
                        *args,
                        **kwargs
                    ),
                    width=input_width,
                )
            ],
            row=row
        )

        return f

    @decorators.wrap_component_with_breaks()
    def dropdown_select(
            self,
            id: str,
            options: List[dict],
            value: Optional[Any] = None,
            classes_to_attach: List[str] = None,
            *args,
            **kwargs
    ):
        classes_to_attach = self.make_classes(classes_to_attach)

        if value is None:
            value = options[0]['label']

        component = dbc.Select(
            id=id,
            options=options,
            value=value,
            className=classes_to_attach,
            *args,
            **kwargs
        )

        return component

    def layout(
            self,
            make_dash_component: bool = None,
            *args,
            **kwargs
    ):
        raise NotImplementedError("Method layout not implemented in BaseLayout class.")
