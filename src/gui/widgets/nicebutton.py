from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

class NiceButton(QPushButton):
    # button color to blue
    # text color to white
    # full rounded corner
    # when hover, scale up by 1.3
    # when clicked, scale up by 1.4
    # when clicked, change color to red
    # when clicked, change text color to black
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: rgb(124, 58, 237);
                color: white;
                border-radius: 15px;
                font-size: 17px;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: rgb(139, 92, 246);
                color: white;
            }
            QPushButton:pressed {
                background-color: rgb(91, 33, 182);
            }
        """)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
