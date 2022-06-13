from dataclasses import dataclass, field
from numbers import Complex
from tkinter import W

import numpy as np

from gradient import Gradient

RE_START = -2
RE_END = 1
IM_START = -1
IM_END = 1


@dataclass(frozen=True)
class Mandelbrot:
    max_iterations: int = 80
    start: complex = field(default_factory=lambda: complex(-2, -1))
    end: complex = field(default_factory=lambda: complex(1, 1))

    def __call__(self, step: complex) -> int:
        z, n = 0, 0
        while abs(z) <= 2 and n < self.max_iterations:
            z = z * z + step
            n += 1 
        return n

    def __get_step(self, width: int, height: int, x: int, y: int) -> complex:
        return complex(self.start.real + (x / width) * (self.end.real - self.start.real),
            self.start.imag + (y / height) * (self.end.imag - self.start.imag))

    def generate(
            self, 
            width: int, 
            height: int,
            gradient: Gradient = None) -> np.ndarray:
        if not gradient:
            gradient = Gradient((0, 0, 0), (255, 255, 255))
        image = np.zeros((height, width, 3), dtype=np.uint8)
        for x in range(width):
            for y in range(height):
                value = self.__call__(self.__get_step(width, height, x, y))
                color = 255 - value * 255 // self.max_iterations
                image[y, x] = gradient(255 - color)
        return image
