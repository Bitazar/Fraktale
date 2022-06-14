from ctypes import c_void_p, c_double

from gradient import Gradient
from lib import library

import numpy as np


class BarnsleyFern:
    def __init__(self, points: int = 800_000) -> None:
        self.__points = points
        self.__obj = library.create_barnsley_fern(points)

    def generate(
            self,
            width: int,
            height: int,
            gradient: Gradient = None) -> np.ndarray:
        if gradient is None:
            gradient = Gradient((0, 0, 0), (255, 255, 255))
        image = np.zeros((height, width, 3), dtype=np.uint8)
        library.generate_barnsley(self.__obj,
            image.ctypes.data_as(c_void_p),
            width, height, gradient.ctype)
        return image

    def generate_parallel(
            self,
            width: int,
            height: int,
            threads: int,
            gradient: Gradient = None) -> np.ndarray:
        if gradient is None:
            gradient = Gradient((0, 0, 0), (255, 255, 255))
        image = np.zeros((height, width, 3), dtype=np.uint8)
        library.generate_barnsley_fern(self.__obj,
            image.ctypes.data_as(c_void_p),
            width, height, gradient.ctype, threads)
        return image

    @property
    def spaceious(self) -> bool:
        return False

    @property
    def points(self) -> int:
        return self.__points

    @points.setter
    def points(self, value: int) -> None:
        if value == self.__points:
            return None
        self.__points = value
        library.set_barnsley_fern_points(self.__obj, value)
