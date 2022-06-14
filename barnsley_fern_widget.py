from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton
from PySide6.QtGui import QIntValidator

from barnsley_fern import BarnsleyFern


class BarnsleyFernWidget(QWidget):
    def __init__(self, fractal: BarnsleyFern) -> None:
        super().__init__()
        self.__fractal = fractal
        self.__iterations = self.__fractal.points
        self.__layout = QVBoxLayout(self)
        self.__layout.addWidget(QLabel('Parametry paprotki Barnsleya'))
        self.__createMaxIter()

    def __reset(self) -> None:
        self.__iterations = 800_000
        self.__layout.itemAt(1).widget().layout().itemAt(1).widget().setText(str(self.__iterations))

    def __createMaxIter(self) -> None:
        def setIterations() -> None:
            self.__iterations = int(edit.text())
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(QLabel('Ilość iteracji'))
        edit = QLineEdit()
        edit.setText(str(self.__iterations))
        edit.setValidator(QIntValidator(1, 1_000_000))
        edit.editingFinished.connect(setIterations)
        layout.addWidget(edit)
        button = QPushButton('Reset')
        button.clicked.connect(self.__reset)
        layout.addWidget(button)
        self.__layout.addWidget(widget)

    def activate(self) -> None:
        self.__fractal.points = self.__iterations