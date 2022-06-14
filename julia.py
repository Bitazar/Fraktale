from concurrent.futures import thread
from ctypes import c_void_p, c_double

from gradient import Gradient
from lib import library

import numpy as np


class Julia:
    def __init__(self, constant: complex = None, max_iterations: int = 80, start: complex = None, end: complex = None) -> None:
        self.__start = start if start else complex(-1, -1)
        self.__end = end if end else complex(1, 1)
        self.__constant = constant if constant else complex(0.285, 0.01)
        self.__maxIterations = max_iterations
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
        library.generate_julia(self.__obj,
            image.ctypes.data_as(c_void_p),
            width, height, gradient.ctype, 8)
        return image

    def generate_parallel(
            self,
            width: int,
            height: int,
            threads: int,
            gradient: Gradient = None) -> np.ndarray:
        if gradient is None:
            gradient = Gradient((0, 127, 127), (255, 255, 255), True)
        image = np.zeros((height, width, 3), dtype=np.uint8)
        library.generate_julia_parallel(self.__obj,
            image.ctypes.data_as(c_void_p),
            width, height, gradient.ctype, threads)
        return image

    @property
    def maxIterations(self) -> int:
        return self.__maxIterations

    @property
    def start(self) -> complex:
        return self.__start

    @property
    def end(self) -> complex:
        return self.__end

    @property
    def constant(self) -> complex:
        return self.__constant

    @maxIterations.setter
    def maxIterations(self, value: int) -> None:
        if value == self.__maxIterations:
            return None
        self.__maxIterations = value
        library.set_julia_max_iter(self.__obj, self.__maxIterations)

    @start.setter
    def start(self, value: complex) -> None:
        if value == self.__start:
            return None
        self.__start = value
        library.set_julia_start(self.__obj, c_double(value.real), c_double(value.imag))

    @end.setter
    def end(self, value: complex) -> None:
        if value == self.__end:
            return None
        self.__end = value
        library.set_julia_end(self.__obj, c_double(value.real), c_double(value.imag))

    @constant.setter
    def constant(self, value: complex) -> None:
        if value == self.__constant:
            return None
        self.__constant = value
        library.set_julia_constant(self.__obj, c_double(value.real), c_double(value.imag))
