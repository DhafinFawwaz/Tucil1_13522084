from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QBoxLayout
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from widgets.normaltext import NormalText
from widgets.numberinput import NumberInput
from widgets.tokeninput import TokenInput
from data.data import Data
from PyQt5 import QtCore

class VContainer(QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            VContainer {
                background-color: rgb(15, 23, 42);
                color: white;
                border-radius: 15px;
                font-size: 15px;
                font-weight: bold;
                padding: 10px 20px;
            }
        """)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)

    def addLayout(self, layout: QBoxLayout):
        self.v_layout.addLayout(layout)
    def addWidget(self, widget: QWidget):
        self.v_layout.addWidget(widget)
    def addStretch(self):
        self.v_layout.addStretch()


        

