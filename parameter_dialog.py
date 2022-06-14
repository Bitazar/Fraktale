from typing import Optional, Tuple

from PySide6.QtWidgets import (
    QDialog, QSlider, QWidget, QDialogButtonBox,
    QVBoxLayout, QLabel, QHBoxLayout
)

from PySide6.QtCore import Signal, QObject

from sliders_widget import *
from gradient import Gradient


class BoundSignals(QObject):
    lowerBound: Signal = Signal(object)
    upperBound: Signal = Signal(object)

LABELS = {
    'RGB': ['Czerwony', 'Zielony', 'Niebieski']
}


class ParameterDialog(QDialog):
    def __init__(self, gradient: Gradient, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.__lowerLimit, self.__upperLimit = gradient.lower_limit, gradient.upper_limit
        self.setWindowTitle("Opcje")
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        self.__signals = BoundSignals()
        self.__signals.lowerBound.connect(self.__changeLowerLimit)
        self.__signals.upperBound.connect(self.__changeUpperLimit)
        self.__innerWidget = QWidget()
        self.__innerLayout = QHBoxLayout(self.__innerWidget)
        self.__innerLayout.addWidget(SlidersWidget('Dolny kolor', self.__lowerLimit, self.__signals.lowerBound, LABELS['RGB']))
        self.__innerLayout.addWidget(SlidersWidget('Górny kolor', self.__upperLimit, self.__signals.upperBound, LABELS['RGB']))
        self.layout.addWidget(self.__innerWidget)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def __changeLowerLimit(self, newValues: object) -> None:
        self.__lowerLimit = newValues

    def __changeUpperLimit(self, newValues: object) -> None:
        self.__upperLimit = newValues

    @property
    def lowerLimit(self) -> Tuple[int]:
        return self.__lowerLimit

    @property
    def upperLimit(self) -> Tuple[int]:
        return self.__upperLimit

