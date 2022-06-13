from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
from PySide6.QtGui import QImage, QPixmap

from mainWindow import Ui_MainWindow
from parameter_dialog import ParameterDialog

import sys

from mandelbrot import Mandelbrot


# Image size (pixels)
WIDTH = 600
HEIGHT = 400


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self.__fractal = Mandelbrot()
        self.__ui.generatingButton.clicked.connect(self.__generate_fractal)
        self.__ui.pushButton.clicked.connect(self.__change_parameters)

    def __change_parameters(self) -> None:
        dialog = ParameterDialog(self)
        dialog.exec()

    def __generate_fractal(self) -> None:
        image = self.__fractal.generate(WIDTH, HEIGHT)
        image = QImage(image.data, WIDTH, HEIGHT, 3 * WIDTH, QImage.Format_RGB888)
        self.__ui.fractalWindow.setPixmap(QPixmap(image))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
