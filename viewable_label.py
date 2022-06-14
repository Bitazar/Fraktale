from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Slot
from PySide6.QtGui import QWheelEvent


class ViewableLabel(QLabel):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.__fractal = None
        self.__factor1 = 0.8
        self.__factor2 = 1.25

    def setFractal(self, fractal) -> None:
        self.__fractal = fractal

    def attachHandle(self, signal) -> None:
        self.__signal = signal

    @Slot()
    def wheelEvent(self, event: QWheelEvent) -> None:
        super().wheelEvent(event)
        if not self.__fractal.spaceious:
            return None
        d = self.__fractal.end - self.__fractal.start
        rx = event.position().x() / self.width()
        ry = event.position().y() / self.height()
        px = d.real * rx + self.__fractal.start.real
        py = d.imag * ry + self.__fractal.start.imag
        new_diagonal = (self.__fractal.end - self.__fractal.start) / 2
        new_diagonal = new_diagonal * (self.__factor1 if event.angleDelta().y() > 0 else self.__factor2)
        self.__fractal.start = complex(px - new_diagonal.real, py - new_diagonal.imag)
        self.__fractal.end = complex(px + new_diagonal.real, py + new_diagonal.imag)
        self.__signal()
