from cv2 import line
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSlider, QLineEdit
from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtGui import QIntValidator

from functools import wraps
from typing import List, Optional, Callable, Tuple


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

    def __createSlider(self, index: int) -> None:
        slider = QSlider()
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(16)
        slider.setMinimum(0)
        slider.setMaximum(255)
        slider.setSliderPosition(self._values[index])
        slider.valueChanged.connect(self.__sliderChangeWrapper(index))
        return slider

    def _setSliders(self, labels: List[str]) -> None:
        self._functions = []
        for i, label in enumerate(labels):
            sliderLayout = QVBoxLayout()
            slider = self.__createSlider(i)
            self._sliders.append(slider)
            label = QLabel(label)
            label.setAlignment(Qt.AlignHCenter)
            sliderLayout.addWidget(label)
            sliderLayout.addWidget(slider, alignment=Qt.AlignHCenter)
            lineEdit = QLineEdit()
            lineEdit.setText(f'{self._values[i]}')
            lineEdit.setValidator(QIntValidator(0, 255))
            lineEdit.setMaximumWidth(35)
            lineEdit.editingFinished.connect(self.__lineEditChanged(i, lineEdit))
            sliderLayout.addWidget(lineEdit, alignment=Qt.AlignHCenter)
            self._sliderLayout.addLayout(sliderLayout)

    @Slot(object)
    def __onSliderChange(self, value: int, index: int) -> None:
        self._values = list(self._values)
        self._values[index] = value
        self._values = tuple(self._values)
        self._sliderLayout.itemAt(index).itemAt(2).widget().setText(str(value))
        self._signal.emit(self._values)

    def __sliderChangeWrapper(self, index: int) -> Callable[[int], None]:
        @Slot(object)
        @wraps(self.__onSliderChange)
        def handler(value: int) -> None:
            return self.__onSliderChange(value, index)
        return handler

    @Slot(object)
    def __onInputChanged(self, index: int, lineEdit: QLineEdit) -> None:
        self._values = list(self._values)
        self._values[index] = int(lineEdit.text())
        self._values = tuple(self._values)
        self._sliderLayout.itemAt(index).itemAt(1).widget().setSliderPosition(int(lineEdit.text()))
        self._signal.emit(self._values)

    def __lineEditChanged(self, index: int, lineEdit: QLineEdit) -> Callable[[], None]:
        @Slot(object)
        @wraps(self.__onInputChanged)
        def handler() -> None:
            return self.__onInputChanged(index, lineEdit)
        return handler

    def changeLabels(self, labels: str) -> None:
        for i, value in enumerate(labels):
            self._sliderLayout.itemAt(i).itemAt(0).widget().setText(value)
