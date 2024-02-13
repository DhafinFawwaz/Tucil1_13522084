from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from widgets.normaltext import NormalText
from widgets.numberinput import NumberInput
from widgets.tokeninput import TokenInput
from data.data import Data
from PyQt5 import QtCore
from models.token_types import Sequence, Token
from models.custom_c_types import C_MarkableToken, C_Token
from ctypes import cdll, CDLL, c_void_p, c_int, c_float, c_double, POINTER, c_char_p, c_bool, c_char, Structure, Array, _Pointer


class SequenceInput(QWidget):

    def on_count_changed(self, text: str):
        if text.isdigit():
            self.count = int(text)
            self.set_sequence_length(self.count)


    def on_reward_changed(self, text: str):
        if text.isdigit():
            self.reward = int(text)

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.count = 3
        self.reward = 15        


        self.setStyleSheet("""
            SequenceInput {
                background-color: rgb(15, 23, 42);
                color: white;
                border-radius: 15px;
                font-size: 15px;
                font-weight: bold;
                padding: 10px 20px;
            }
        """)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)
        self.h_layout.setSpacing(Data.padding_1)

        self.reward_label = NormalText(None, "Reward: ")
        self.reward_input = NumberInput(None, 0)
        self.reward_input.setText(str(self.reward))
        self.reward_input.setFixedWidth(40)
        self.h_layout.addWidget(self.reward_label)
        self.h_layout.addWidget(self.reward_input)
        self.reward_input.textChanged.connect(self.on_reward_changed)
        
        self.count_label = NormalText(None, "Length: ")
        self.count_input = NumberInput(None, 0)
        self.count_input.setText(str(self.count))
        self.count_input.set_allow_negative_or_zero(False)
        self.count_input.setFixedWidth(40)
        self.h_layout.addWidget(self.count_label)
        self.h_layout.addWidget(self.count_input)
        self.count_input.textChanged.connect(self.on_count_changed)

        self.reward_label = NormalText(None, "Sequence: ")
        self.h_layout.addWidget(self.reward_label)

        self.sequence_layout = QHBoxLayout()
        self.h_layout.addLayout(self.sequence_layout)

        self.inputs: list[TokenInput] = []
        
        self.set_sequence_length(self.count)

    def set_sequence_length(self, new_length: int):
        for i in reversed(range(self.sequence_layout.count())): 
            item = self.sequence_layout.itemAt(i).spacerItem()
            if item != None:
                self.sequence_layout.removeItem(item)
                continue
            widget = self.sequence_layout.itemAt(i).widget()
            if widget != None:
                widget.deleteLater()
            

        self.count = new_length
        self.inputs = []

        for i in range(self.count):
            token_input = TokenInput(self, "FF")
            self.sequence_layout.addWidget(token_input)
            self.inputs.append(token_input)
        self.sequence_layout.addStretch()

    def get_element(self, i: int) -> str:
        return self.inputs[i].text()

    def get_sequence_c(self) -> Array[C_Token]:
        token_sequence = (C_Token * self.count)()
        for j in range(self.count):
            token_sequence[j] = C_Token(self.get_element(j))
        return token_sequence

        

