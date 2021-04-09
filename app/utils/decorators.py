from dash_html_components import Br
from typing import *


def attach_classes(f):
    def wrapper_function(*args, **kwargs):
        classes_to_attach = kwargs.pop("classes_to_attach", None)
        if classes_to_attach is None:
            classes_to_attach = []
        classes_to_attach = " ".join(classes_to_attach)
        return f(classes_to_attach=classes_to_attach, *args, **kwargs)
    return wrapper_function


def use_default_classes(default_classes: str):
    # take in a string to avoid initializing arrays since they are mutable
    default_classes = default_classes.split(" ")

    def wrapper(f):
        def w(*args, **kwargs):
            return f(*args, **kwargs, default_classes=default_classes)
        return w
    return wrapper


def wrap_component_with_breaks(n_before: int = 1, n_after: int = 1):
    def wrapper(f):
        def w(*args, **kwargs):
            output_component = f(*args, **kwargs)
            output = [
                *[Br() for i in range(n_before)],
                output_component,
                *[Br() for i in range(n_after)]
            ]
            return output
        return w
    return wrapper
