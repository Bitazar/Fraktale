from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PySide6.QtGui import QImage, QPixmap
from barnsley_fern_widget import BarnsleyFernWidget
from execution_widget import Execution
import cv2

from gradient import Gradient
from julia_widget import JuliaWidget
from mainWindows import Ui_Fraktale
from mandelbrot_widget import MandelbrotWidget
from parameter_dialog import ParameterDialog
from julia import Julia
from barnsley_fern import BarnsleyFern
from mandelbrot import Mandelbrot

import sys


FRACTALS = [
    Mandelbrot(),
    Julia(),
    BarnsleyFern()
]


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.__execution = Execution(Execution.Modes.Parallel, 8)
        self.__dimensions = [600, 400]
        self.__image = None
        self.__ui = Ui_Fraktale()
        self.__ui.setupUi(self)
        self.__ui.comboBox.currentIndexChanged.connect(self.__change_fractal)
        self.__fractal = FRACTALS[0]
        self.__gradient = Gradient([0, 0, 0], [0, 255, 0])
        self.__ui.generatingButton.clicked.connect(self.__generate_fractal)
        self.__ui.pushButton.clicked.connect(self.__change_parameters)
        self.__ui.saveButton.clicked.connect(self.__saveToFile)

    def __saveToFile(self) -> QWidget:
        if self.__image is None:
            return None
        filename, _ = QFileDialog.getSaveFileName(
            QApplication.activeWindow())
        if filename.split('.')[-1].lower() not in ['jpg', 'jpeg', 'png']:
            return None
        cv2.imwrite(filename, cv2.cvtColor(self.__image, cv2.COLOR_RGB2BGR))

    def __getWidget(self) -> QWidget:
        if isinstance(self.__fractal, Mandelbrot):
            return MandelbrotWidget(self.__fractal)
        elif isinstance(self.__fractal, Julia):
            return JuliaWidget(self.__fractal)
        elif isinstance(self.__fractal, BarnsleyFern):
            return BarnsleyFernWidget(self.__fractal)
        return None

    def __change_fractal(self, index: int) -> None:
        self.__fractal = FRACTALS[index]

    def __change_parameters(self) -> None:
        dialog = ParameterDialog(
            self.__gradient,
            self.__dimensions,
            self.__getWidget(),
            self.__execution,
            self)
        if dialog.exec():
            self.__gradient.lower_limit = dialog.lowerLimit
            self.__gradient.upper_limit = dialog.upperLimit
            self.__gradient.system = dialog.system
            self.__gradient.inverted = dialog.inverted
            self.__dimensions = dialog.dimensions
            dialog.activateWidget()

    def __generate_fractal(self) -> None:
        width, height = self.__dimensions
        if self.__execution.mode == Execution.Modes.Sequenced:
            image = self.__fractal.generate(*self.__dimensions, self.__gradient)
        else:
            image = self.__fractal.generate_parallel(*self.__dimensions, self.__execution.threads, self.__gradient)
        self.__image = image
        image = QImage(image.data, width, height, 3 * width, QImage.Format_RGB888)
        self.__ui.fractalWindow.setPixmap(QPixmap(image))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
