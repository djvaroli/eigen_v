from components.BaseComponent import BaseComponent


class HomeComponent(BaseComponent):
    title = "Home"

    def layout(
            self,
            make_dash_component: bool = None,
            *args,
            **kwargs
    ):
