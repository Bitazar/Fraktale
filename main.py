from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
from PySide6.QtGui import QImage, QPixmap

from gradient import Gradient

from mainWindows import Ui_Fraktale
from parameter_dialog import ParameterDialog

import sys

from julia import Julia
from barnsley_fern import BarnsleyFern
from mandelbrot import Mandelbrot


# Image size (pixels)
WIDTH = 600
HEIGHT = 400

FRACTALS = [
    Mandelbrot(),
    Julia(),
    BarnsleyFern()
]


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.__ui = Ui_Fraktale()
        self.__ui.setupUi(self)
        self.__ui.comboBox.currentIndexChanged.connect(self.__change_fractal)
        self.__fractal = FRACTALS[0]
        self.__gradient = Gradient([0, 0, 0], [255, 255, 255])
        self.__ui.generatingButton.clicked.connect(self.__generate_fractal)
        self.__ui.pushButton.clicked.connect(self.__change_parameters)

    def __change_fractal(self, index: int) -> None:
        self.__fractal = FRACTALS[index]

    def __change_parameters(self) -> None:
        dialog = ParameterDialog(self.__gradient, self)
        if dialog.exec():
            self.__gradient.lower_limit = dialog.lowerLimit
            self.__gradient.upper_limit = dialog.upperLimit
            self.__gradient.system = dialog.system
            self.__gradient.inverted = dialog.inverted

    def __generate_fractal(self) -> None:
        image = self.__fractal.generate(WIDTH, HEIGHT, self.__gradient)
        image = QImage(image.data, WIDTH, HEIGHT, 3 * WIDTH, QImage.Format_RGB888)
        self.__ui.fractalWindow.setPixmap(QPixmap(image))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
