from dataclasses import dataclass
from typing import Tuple


Color = Tuple[int, int, int]

@dataclass(frozen=True)
class Gradient:
    lower_limit: Color
    upper_limit: Color

    def __interpolate(self, value: int, axis: int) -> int:
        int_range = self.upper_limit[axis] - self.lower_limit[axis]
        value = self.lower_limit[axis] + int_range * value // 255
        return (value if value < 256 else 255) if value >= 0 else 0

    def __call__(self, value: int) -> Color:
        return tuple([ 
            self.__interpolate(value, axis) for axis in range(3)
        ])
