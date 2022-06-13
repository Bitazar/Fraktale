from ctypes import c_void_p, c_double, c_uint8
from typing import Tuple

from lib import library


Color = Tuple[int, int, int]


class Gradient:
    def __init__(self, lower_limit: Color, upper_limit: Color) -> None:
        self.__lower_limit = lower_limit
        self.__upper_limit = upper_limit
        self.__gradient = library.generate_gradient(
            c_uint8(lower_limit[0]),
            c_uint8(lower_limit[1]),
            c_uint8(lower_limit[2]),
            c_uint8(upper_limit[0]),
            c_uint8(upper_limit[1]),
            c_uint8(upper_limit[2])
        )

    @property
    def ctype(self) -> int:
        return self.__gradient
