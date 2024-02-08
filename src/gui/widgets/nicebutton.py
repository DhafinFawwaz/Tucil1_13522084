from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

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
                background-color: #3498db;
                color: white;
                border-radius: 15px;
                font-size: 17px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5dade2;
                color: white;
                border-radius: 15px;
                border: 2px solid #5dade2;
            }
            QPushButton:pressed {
                background-color: #ec7063;
                color: black;
                border-radius: 15px;
                border: 2px solid #ec7063;
            }
        """)