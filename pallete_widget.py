from tkinter import Button
from typing import Dict, Callable, TypeVar

from PySide6.QtWidgets import QWidget, QButtonGroup, QRadioButton, QVBoxLayout, QLabel
from PySide6.QtCore import Slot, Signal

from functools import wraps

from gradient import System

BoundSignals = TypeVar('BoundSignals')


class PalleteWidget(QWidget):
    def __init__(
            self,
            title: str,
            initial_system: System,
            signals: BoundSignals,
            palletes: Dict[str, System],
            inverted: bool,
            parent: QWidget = None) -> None:
        super().__init__(parent)
        self.__signals = signals
        self.__butonGroup = QButtonGroup(self)
        self.__layout = QVBoxLayout(self)
        self.__label = QLabel(title)
        self.__layout.addWidget(self.__label)
        for key, system in palletes.items():
            button = QRadioButton()
            button.setText(str(key))
            button.system = system
            if system == initial_system:
                button.setChecked(True)
            button.clicked.connect(self.__buttonChangeWrapper(button, True))
            self.__layout.addWidget(button)
            self.__butonGroup.addButton(button)
        self.__layout.addWidget(QLabel('Odwrócenie kolorów'))
        button = QRadioButton()
        button.setText('Odwrócone kolory')
        if inverted:
            button.setChecked(True)
        button.clicked.connect(self.__buttonChangeWrapper(button, False))
        self.__layout.addWidget(button)

    @Slot(object)
    def __onButtonClick(self, button: QRadioButton) -> None:
        self.__signals.pallete.emit(button.system)

    def __buttonChangeWrapper(self, button: QRadioButton, type: bool) -> Callable[[QRadioButton], None]:
        @Slot(object)
        @wraps(self.__onButtonClick)
        def handler(value: int) -> None:
            if type:
                return self.__onButtonClick(button)
            return self.__onInversion(button)
        return handler

    @Slot(object)
    def __onInversion(self, button: QRadioButton) -> None:
        self.__signals.invert.emit(button.isChecked())
