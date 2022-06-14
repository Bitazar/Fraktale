from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Slot, Qt, Signal

from functools import wraps
from typing import Tuple, Callable


class SizeWidget(QWidget):
    def __init__(self, dimensions: Tuple[int], signals, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.__layout = QVBoxLayout(self)
        self.__layout.addWidget(QLabel('Rozmiar okna'))
        self.__layout.addWidget(self.__createEdit('Długość okna', dimensions[0], 4096, signals.changeWidth))
        self.__layout.addWidget(self.__createEdit('Szerokość okna', dimensions[1], 3112, signals.changeHeight))

    def __createEdit(self, title: str, default: int, lock: int, signal) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(QLabel(title))
        lineEdit = QLineEdit(str(default))
        lineEdit.setValidator(QIntValidator(0, lock))
        lineEdit.editingFinished.connect(self.__editChangeWrapper(lineEdit, signal))
        layout.addWidget(lineEdit)
        return widget

    @Slot(object)
    def __onEditChange(self, lineEdit: QLineEdit, signal) -> None:
        signal.emit(int(lineEdit.text()))

    def __editChangeWrapper(self, lineEdit: QLineEdit, signal) -> Callable[[QLineEdit], None]:
        @Slot(object)
        @wraps(self.__onEditChange)
        def handler() -> None:
            return self.__onEditChange(lineEdit, signal)
        return handler
