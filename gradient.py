from ctypes import c_void_p, c_double, c_uint8, c_bool
import sys
from typing import Tuple
from enum import Enum

from lib import library


Color = Tuple[int, int, int]


class System(Enum):
    RGB = 0x01,
    HSV = 0x02,
    YCbCr = 0x03,
    YUV = 0x04


class Gradient:
    def __init__(self, lower_limit: Color, upper_limit: Color, inverted: bool = False) -> None:
        self.__lower_limit = lower_limit
        self.__upper_limit = upper_limit
        self.__gradient = library.generate_gradient(
            c_uint8(lower_limit[0]),
            c_uint8(lower_limit[1]),
            c_uint8(lower_limit[2]),
            c_uint8(upper_limit[0]),
            c_uint8(upper_limit[1]),
            c_uint8(upper_limit[2]),
            c_bool(inverted)
        )

    @property
    def ctype(self) -> int:
        return self.__gradient

    def change_system(self, system: System) -> None:
        library.change_gradient_system(self.ctype, c_uint8(system.value[0]))
