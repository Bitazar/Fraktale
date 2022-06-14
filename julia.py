from ctypes import c_void_p, c_double

from gradient import Gradient
from lib import library

import numpy as np


class Julia:
    def __init__(self, constant: complex = None, max_iterations: int = 80, start: complex = None, end: complex = None) -> None:
        self.__start = start if start else complex(-2, -1)
        self.__end = end if end else complex(1, 1)
        self.__constant = constant if constant else complex(0.285, 0.01)
        self.__obj = library.create_julia(
            max_iterations, c_double(self.__start.real), c_double(self.__start.imag),
            c_double(self.__end.real), c_double(self.__end.imag),
            c_double(self.__constant.real), c_double(self.__constant.imag)
        )

    def generate(
            self,
            width: int,
            height: int,
            gradient: Gradient = None) -> np.ndarray:
        if gradient is None:
            gradient = Gradient((0, 127, 127), (255, 255, 255), True)
        image = np.zeros((height, width, 3), dtype=np.uint8)
        library.generate_julia_parallel(self.__obj,
            image.ctypes.data_as(c_void_p),
            width, height, gradient.ctype, 8)
        return image
