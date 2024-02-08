from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QSizePolicy, QLineEdit
from PyQt5 import QtCore

class NumberInput(QLineEdit):
    def __init__(self, parent: QWidget, value: int):
        super().__init__(parent)
        self.setStyleSheet("""
            QLineEdit {
                color: white;
                font-size: 14px;
                font-weight: bold;
                background-color: #444;
                max-width: 100px;
                border-radius: 10px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #5dade2;
            }
        """)
        # left
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.textChanged.connect(self.on_text_changed)
        self.old_text = ""
        
    def on_text_changed(self, text):

        if text == "":
            return
        if not text.isdigit():
            self.setText(self.old_text)
        else:
            self.setText(text)
            self.old_text = text
        