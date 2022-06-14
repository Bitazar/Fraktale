from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton
from PySide6.QtCore import Slot
from PySide6.QtGui import QIntValidator, QDoubleValidator

from functools import wraps
from typing import Callable

from mandelbrot import Mandelbrot

class MandelbrotWidget(QWidget):
    def __init__(self, fractal: Mandelbrot) -> None:
        super().__init__()
        self.__fractal = fractal
        self.__start = [fractal.start]
        self.__end = [fractal.end]
        self.__iterations = self.__fractal.maxIterations
        self.__layout = QVBoxLayout(self)
        self.__layout.addWidget(QLabel('Parametry zbioru Mandelbrota'))
        self.__createComplex('Początek', self.__start)
        self.__createComplex('Koniec', self.__end)
        self.__createMaxIter()

    def __createComplex(self, title: str, value: complex) -> None:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(QLabel(f'{title} - część rzeczywista'))
        realEdit = QLineEdit()
        realEdit.setText(str(value[0].real))
        realEdit.setValidator(QDoubleValidator(-5000., 5000., 10))
        realEdit.editingFinished.connect(self.__editChangeWrapper(value, realEdit, True))
        layout.addWidget(realEdit)
        layout.addWidget(QLabel(f'{title} - część urojona'))
        imagEdit = QLineEdit()
        imagEdit.setText(str(value[0].imag))
        imagEdit.setValidator(QDoubleValidator(-5000., 5000., 10))
        imagEdit.editingFinished.connect(self.__editChangeWrapper(value, imagEdit, False))
        layout.addWidget(imagEdit)
        self.__layout.addWidget(widget)

    def __reset(self) -> None:
        self.__start[0] = complex(-2, -1)
        self.__end[0] = complex(1, 1)
        self.__iterations = 80
        self.__layout.itemAt(1).widget().layout().itemAt(1).widget().setText(str(self.__start[0].real))
        self.__layout.itemAt(1).widget().layout().itemAt(3).widget().setText(str(self.__start[0].imag))
        self.__layout.itemAt(2).widget().layout().itemAt(1).widget().setText(str(self.__end[0].real))
        self.__layout.itemAt(2).widget().layout().itemAt(3).widget().setText(str(self.__end[0].imag))
        self.__layout.itemAt(3).widget().layout().itemAt(1).widget().setText(str(self.__iterations))

    def __createMaxIter(self) -> None:
        def setIterations() -> None:
            self.__iterations = int(edit.text())
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(QLabel('Maksymalna ilość iteracji'))
        edit = QLineEdit()
        edit.setText(str(self.__iterations))
        edit.setValidator(QIntValidator(1, 1_000_000))
        edit.editingFinished.connect(setIterations)
        layout.addWidget(edit)
        button = QPushButton('Reset')
        button.clicked.connect(self.__reset)
        layout.addWidget(button)
        self.__layout.addWidget(widget)

    @Slot(object)
    def __onEditChange(self, number: complex, lineEdit: QLineEdit, type: bool) -> None:
        if type:
            number[0] = complex(float(lineEdit.text()), number[0].imag)
        else:
            number[0] = complex(number[0].real, float(lineEdit.text()))

    def __editChangeWrapper(self, number: complex, lineEdit: QLineEdit, type: bool) -> Callable[[QLineEdit], None]:
        @Slot(object)
        @wraps(self.__onEditChange)
        def handler() -> None:
            return self.__onEditChange(number, lineEdit, type)
        return handler

    def activate(self) -> None:
        self.__fractal.start = self.__start[0]
        self.__fractal.end = self.__end[0]
