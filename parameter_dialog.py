from typing import Optional
from PySide6.QtWidgets import (
    QDialog, QSlider, QWidget, QDialogButtonBox,
    QVBoxLayout, QLabel
)


class ParameterDialog(QDialog):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Opcje")
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def __iteration_dialog(self) -> None:
        self.iter_widget = QWidget()

