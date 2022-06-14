# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_Fraktale(object):
    def setupUi(self, Fraktale):
        if not Fraktale.objectName():
            Fraktale.setObjectName(u"Fraktale")
        Fraktale.resize(800, 600)
        self.centralwidget = QWidget(Fraktale)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)

        self.fractalWindow = QLabel(self.centralwidget)
        self.fractalWindow.setObjectName(u"fractalWindow")
        self.fractalWindow.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.fractalWindow, 2, 0, 1, 2)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 1)

        self.generatingButton = QPushButton(self.centralwidget)
        self.generatingButton.setObjectName(u"generatingButton")

        self.gridLayout.addWidget(self.generatingButton, 3, 0, 1, 1)

        self.saveButton = QPushButton(self.centralwidget)
        self.saveButton.setObjectName(u"saveButton")

        self.gridLayout.addWidget(self.saveButton, 3, 1, 1, 1)

        Fraktale.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Fraktale)
        self.statusbar.setObjectName(u"statusbar")
        Fraktale.setStatusBar(self.statusbar)

        self.retranslateUi(Fraktale)

        QMetaObject.connectSlotsByName(Fraktale)
    # setupUi

    def retranslateUi(self, Fraktale):
        Fraktale.setWindowTitle(QCoreApplication.translate("Fraktale", u"Fraktale", None))
        self.pushButton.setText(QCoreApplication.translate("Fraktale", u"Opcje", None))
        self.fractalWindow.setText("")
        self.comboBox.setItemText(0, QCoreApplication.translate("Fraktale", u"Zbi\u00f3r Mandelbrota", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Fraktale", u"Zbi\u00f3r Julii", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Fraktale", u"Papro\u0107 Barnsleya", None))

        self.generatingButton.setText(QCoreApplication.translate("Fraktale", u"Generuj", None))
        self.saveButton.setText(QCoreApplication.translate("Fraktale", u"Zapisz do pliku", None))
    # retranslateUi

