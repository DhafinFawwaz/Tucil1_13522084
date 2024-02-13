from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QSizePolicy, QLineEdit
from PyQt5 import QtCore

class NumberInput(QLineEdit):
    
    def __init__(self, parent: QWidget, value: int):
        super().__init__(parent)
        self.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                color: white;
                font-size: 14px;
                font-weight: bold;
                background-color: rgb(30, 41, 59);
                border-radius: 10px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 2px solid rgb(139, 92, 246);
            }
        """)
        # left
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.textChanged.connect(self.on_text_changed)
        self.old_text = ""
        self.allow_negative_or_zero = True

    def set_allow_negative_or_zero(self, allow_negative: bool):
        self.allow_negative_or_zero = allow_negative


    def on_text_changed(self, text):

        if text == "":
            return
        if text.isdigit() or (text == '-') or (text[0] == '-' and text[1:].isdigit()):
            if self.allow_negative_or_zero:
                self.setText(text)
                self.old_text = text
            else:
                # case '-'
                if len(text) == 1 and text == '-':
                    self.setText(self.old_text)
                    return
                # case '0'
                if len(text) == 1 and text == '0':
                    self.setText(self.old_text)
                    return

                val = int(text)
                if(val >= 0): # not self.allow_negative and 
                    self.setText(text)
                    self.old_text = text
                elif(val < 0): # not self.allow_negative and 
                    self.setText(self.old_text)
        else:
            self.setText(self.old_text)
        