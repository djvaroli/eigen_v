from typing import *


def list_to_string(
        input_list: List[str],
        delimiter: str = " "
) -> str:
    return delimiter.join(input_list)