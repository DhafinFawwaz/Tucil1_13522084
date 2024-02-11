from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QSizePolicy, QLineEdit
from PyQt5 import QtCore

class TokenInput(QLineEdit):
    def __init__(self, parent: QWidget, value: int):
        super().__init__(parent)
        self.setStyleSheet("""
            QLineEdit {
                color: white;
                font-size: 14px;
                font-weight: bold;
                background-color: rgb(30, 41, 59);
                max-width: 40px;
                border-radius: 10px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 2px solid rgb(139, 92, 246);
            }
        """)
        # left
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.textChanged.connect(self.on_text_changed)
        self.old_text = ""
        
    def on_text_changed(self, text):
        if len(text) > 2:
            self.setText(self.old_text)
        else:
            self.setText(text)
            self.old_text = text
        