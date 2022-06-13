from ctypes import cdll, c_void_p, c_double

from gradient import Gradient

import numpy as np


class Mandelbrot:
    def __init__(self, max_iterations: int = 80, start: complex = None, end: complex = None) -> None:
        self.__lib = cdll.LoadLibrary('libbackend.so')
        self.__start = start if start else complex(-2, -1)
        self.__end = end if end else complex(1, 1)
        self.__obj = self.__lib.create_mandelbrot(
            max_iterations, c_double(self.__start.real), c_double(self.__start.imag),
            c_double(self.__end.real), c_double(self.__end.imag)
        )

    def generate(
            self,
            width: int,
            height: int,
            gradient: Gradient = None) -> np.ndarray:
        image = np.zeros((height, width, 3), dtype=np.uint8)
        self.__lib.generate_mandelbrot_parallel(self.__obj,
            image.ctypes.data_as(c_void_p),
            width, height, 8)
        return image
