from ctypes import c_void_p, c_double, c_uint8, c_bool
import sys
from typing import Tuple
from enum import Enum

from lib import library


Color = Tuple[int, int, int]


class System(Enum):
    RGB = 0x01
    HSV = 0x02
    YCbCr = 0x04
    YUV = 0x08


class Gradient:
    def __init__(self, lower_limit: Color, upper_limit: Color, inverted: bool = False) -> None:
        self.__lower_limit = lower_limit
        self.__upper_limit = upper_limit
        self.__inverted = inverted
        self.__system = None
        self.__gradient = library.generate_gradient(
            c_uint8(lower_limit[0]),
            c_uint8(lower_limit[1]),
            c_uint8(lower_limit[2]),
            c_uint8(upper_limit[0]),
            c_uint8(upper_limit[1]),
            c_uint8(upper_limit[2]),
            c_bool(inverted)
        )
        self.system = System.RGB

    @property
    def ctype(self) -> int:
        return self.__gradient

    def change_system(self, system: System) -> None:
        library.change_gradient_system(self.ctype, c_uint8(system.value))

    @property
    def lower_limit(self) -> Color:
        return self.__lower_limit

    @property
    def upper_limit(self) -> Color:
        return self.__upper_limit

    @property
    def system(self) -> System:
        return self.__system

    @property
    def inverted(self) -> bool:
        return self.__inverted

    @lower_limit.setter
    def lower_limit(self, lower_limit: Color) -> None:
        if lower_limit == tuple(self.__lower_limit):
            return None
        self.__lower_limit = tuple(lower_limit)
        library.gradient_change_lower_limit(
            self.ctype,
            c_uint8(lower_limit[0]),
            c_uint8(lower_limit[1]),
            c_uint8(lower_limit[2]),
        )

    @upper_limit.setter
    def upper_limit(self, upper_limit: Color) -> None:
        if upper_limit == tuple(self.__upper_limit):
            return None
        self.__upper_limit = tuple(upper_limit)
        library.gradient_change_upper_limit(
            self.ctype,
            c_uint8(upper_limit[0]),
            c_uint8(upper_limit[1]),
            c_uint8(upper_limit[2]),
        )

    @system.setter
    def system(self, new_system: System) -> None:
        if self.__system == new_system:
            return None
        self.__system = new_system
        library.change_gradient_system(self.ctype, c_uint8(self.__system.value))

    @inverted.setter
    def inverted(self, value: bool) -> None:
        if self.__inverted == value:
            return None
        self.__inverted = value
        library.invert_gradient(self.ctype)
