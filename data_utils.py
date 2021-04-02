import logging

import numpy as np

CHARS_TO_STRIP = "[]()"
logger = logging.getLogger("data-utils-logger")
logger.setLevel(logging.INFO)


def string_to_numpy(s: str):
    try:
        for char in CHARS_TO_STRIP:
            s = s.replace(char, "")
        s = s.strip().split(",")
        output = np.array(s).astype(np.int32)
    except Exception as e:
        logger.warning(f"{e}")
        output = None

    return output


def string_to_range(s: str, return_list=True):
    try:
        for char in CHARS_TO_STRIP:
            s = s.replace(char, "")
        s = s.strip().split(",")
        output = range(int(s[0]), int(s[1]) + 1)
        if return_list:
            output = list(output)

    except Exception as e:
        logger.warning(f"{e}")
        output = None

    return output
