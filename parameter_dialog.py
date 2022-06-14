from typing import Optional, Tuple

from PySide6.QtWidgets import (
    QDialog, QSlider, QWidget, QDialogButtonBox,
    QVBoxLayout, QLabel, QHBoxLayout
)

from PySide6.QtCore import Signal, QObject

from sliders_widget import SlidersWidget
from pallete_widget import PalleteWidget
from size_widget import SizeWidget
from gradient import Gradient, System


class BoundSignals(QObject):
    lowerBound: Signal = Signal(object)
    upperBound: Signal = Signal(object)
    pallete: Signal = Signal(object)
    invert: Signal = Signal(object)
    changeWidth: Signal = Signal(object)
    changeHeight: Signal = Signal(object)

LABELS = {
    System.RGB: ['Czerwony', 'Zielony', 'Niebieski'],
    System.HSV: ['Odcień', 'Nasycenie', 'Moc'],
    System.YCbCr: ['Luminancja', 'Niebieski', 'Czerwony'],
    System.YUV: ['Luminancja', 'U', 'V']
}

PALLETES = {
    'RGB': System.RGB,
    'HSV': System.HSV,
    'YCbCr': System.YCbCr,
    'YUV': System.YUV
}

class ParameterDialog(QDialog):
    def __init__(self, gradient: Gradient, dimensions: Tuple[int], parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.__system, self.__inverted = gradient.system, gradient.inverted
        self.__lowerLimit, self.__upperLimit = gradient.lower_limit, gradient.upper_limit
        self.__dimensions = dimensions
        self.setWindowTitle("Opcje")
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.__layout = QVBoxLayout()
        self.__signalsCreation()
        self.__innerLayoutCreation(gradient)
        self.__layout.addWidget(self.__innerWidget)
        self.__windowBoxCreation(dimensions)
        self.__layout.addWidget(self.buttonBox)
        self.setLayout(self.__layout)

    def __windowBoxCreation(self, dimensions: Tuple[int]) -> None:
        self.__sizeWidnow = SizeWidget(dimensions, self.__signals)
        self.__signals.changeHeight.connect(self.__changeHeight)
        self.__signals.changeWidth.connect(self.__changeWidth)
        self.__layout.addWidget(self.__sizeWidnow)

    def __signalsCreation(self) -> None:
        self.__signals = BoundSignals()
        self.__signals.lowerBound.connect(self.__changeLowerLimit)
        self.__signals.upperBound.connect(self.__changeUpperLimit)
        self.__signals.pallete.connect(self.__changeSystem)
        self.__signals.invert.connect(self.__invert)

    def __innerLayoutCreation(self, gradient: Gradient) -> None:
        self.__innerWidget = QWidget()
        self.__innerLayout = QHBoxLayout(self.__innerWidget)
        self.__downSlider = SlidersWidget('Dolny kolor', self.__lowerLimit, self.__signals.lowerBound, LABELS[gradient.system])
        self.__upSlider = SlidersWidget('Górny kolor', self.__upperLimit, self.__signals.upperBound, LABELS[gradient.system])
        self.__innerLayout.addWidget(self.__downSlider)
        self.__innerLayout.addWidget(self.__upSlider)
        self.__innerLayout.addWidget(PalleteWidget('Palety kolorów', self.__system, self.__signals, PALLETES, gradient.inverted))

    def __changeLowerLimit(self, newValues: object) -> None:
        self.__lowerLimit = newValues

    def __changeUpperLimit(self, newValues: object) -> None:
        self.__upperLimit = newValues

    def __changeSystem(self, system: System) -> None:
        self.__system = system
        self.__downSlider.changeLabels(LABELS[system])
        self.__upSlider.changeLabels(LABELS[system])

    def __invert(self, direction: bool) -> None:
        self.__inverted = direction

    def __changeWidth(self, width: int) -> None:
        self.__dimensions = (width, self.__dimensions[1])

    def __changeHeight(self, height: int) -> None:
        self.__dimensions = (self.__dimensions[0], height)

    @property
    def lowerLimit(self) -> Tuple[int]:
        return self.__lowerLimit

    @property
    def upperLimit(self) -> Tuple[int]:
        return self.__upperLimit

    @property
    def system(self) -> System:
        return self.__system

    @property
    def inverted(self) -> bool:
        return self.__inverted

    @property
    def dimensions(self) -> Tuple[int]:
        return self.__dimensions

