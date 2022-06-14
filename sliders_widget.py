from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSlider
from PySide6.QtCore import Slot, Qt, Signal

from functools import wraps
from typing import List, Optional, Callable, Tuple

from numpy import array, uint8


class SlidersWidget(QWidget):

    def __init__(
            self,
            widgetName: str,
            positions: Tuple[int],
            signal: Signal(object),
            labels: List[str],
            parent: Optional[QWidget] = None
            ) -> None:
        super().__init__(parent)
        self._values = positions
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(QLabel(widgetName))
        self._signal = signal
        self._sliders = []
        self._sliderWidget = QWidget()
        self._sliderLayout = QHBoxLayout(self._sliderWidget)
        self._setSliders(labels)
        self._layout.addWidget(self._sliderWidget)

    def _setSliders(self, labels: List[str]) -> None:
        self._functions = []
        for i, label in enumerate(labels):
            sliderLayout = QVBoxLayout()
            slider = QSlider()
            slider.setTickPosition(QSlider.TicksBothSides)
            slider.setTickInterval(16)
            slider.setMinimum(0)
            slider.setMaximum(255)
            slider.setSliderPosition(self._values[i])
            slider.valueChanged.connect(self.sliderChangeWrapper(i))
            self._sliders.append(slider)
            label = QLabel(label)
            label.setAlignment(Qt.AlignHCenter)
            valueLabel = QLabel(f'{self._values[i]}')
            valueLabel.setAlignment(Qt.AlignHCenter)
            sliderLayout.addWidget(label)
            sliderLayout.addWidget(slider, alignment=Qt.AlignHCenter)
            sliderLayout.addWidget(valueLabel)
            self._sliderLayout.addLayout(sliderLayout)

    @Slot(object)
    def onSliderChange(self, value: int, index: int) -> None:
        self._values = list(self._values)
        self._values[index] = value
        self._values = tuple(self._values)
        self._sliderLayout.itemAt(index).itemAt(2).widget().setText(str(value))
        self._signal.emit(self._values)

    def sliderChangeWrapper(self, index: int) -> Callable[[int], None]:
        @Slot(object)
        @wraps(self.onSliderChange)
        def handler(value: int) -> None:
            return self.onSliderChange(value, index)
        return handler

    def changeLabels(self, labels: str) -> None:
        for i, value in enumerate(labels):
            self._sliderLayout.itemAt(i).itemAt(2).widget().setText(value)
