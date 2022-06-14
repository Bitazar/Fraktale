from dataclasses import dataclass
from enum import Enum

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QRadioButton, QButtonGroup
from PySide6.QtCore import Slot
from PySide6.QtGui import QIntValidator, QDoubleValidator


@dataclass
class Execution:
    class Modes(Enum):
        Sequenced = 0
        Parallel = 1
    mode: Modes
    threads: int


class ExecutionWidget(QWidget):
    def __init__(self, execution: Execution) -> None:
        super().__init__()
        self.__execution = execution
        self.__threads = self.__execution.threads
        self.__mode = self.__execution.mode
        self.__button_group = QButtonGroup()
        self.__layout = QVBoxLayout(self)
        self.__layout.addWidget(QLabel('Tryb Przetwarzania'))
        self.__sequencedWidget()
        self.__parallelWidget()
        if self.__execution.mode == Execution.Modes.Parallel:
            self.__parallel_button.setChecked(True)
        else:
            self.__sequenced_button.setChecked(True)

    def __parallelButtonCallback(self) -> None:
        self.__mode = Execution.Modes.Parallel
        self.__threads_edit.setDisabled(False)

    def __sequencedButtonCallback(self) -> None:
        self.__mode = Execution.Modes.Sequenced
        self.__threads_edit.setDisabled(True)

    def __editCallback(self) -> None:
        self.__threads = int(self.__threads_edit.text())

    def __sequencedWidget(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        self.__sequenced_button = QRadioButton('Sekwencyjny')
        self.__sequenced_button.clicked.connect(self.__sequencedButtonCallback)
        self.__button_group.addButton(self.__sequenced_button)
        layout.addWidget(self.__sequenced_button)
        self.__layout.addWidget(widget)

    def __parallelWidget(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        self.__parallel_button = QRadioButton('Równoległy')
        self.__parallel_button.clicked.connect(self.__parallelButtonCallback)
        self.__button_group.addButton(self.__parallel_button)
        layout.addWidget(self.__parallel_button)
        self.__threads_edit = QLineEdit()
        self.__threads_edit.setValidator(QIntValidator(0, 100))
        self.__threads_edit.setText(str(self.__execution.threads))
        self.__threads_edit.editingFinished.connect(self.__editCallback)
        if self.__execution.mode == Execution.Modes.Sequenced:
            self.__threads_edit.setDisabled(True)
        layout.addWidget(self.__threads_edit)
        self.__layout.addWidget(widget)

    def activate(self) -> None:
        self.__execution.threads = self.__threads
        self.__execution.mode = self.__mode
