from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from widgets.normaltext import NormalText
from widgets.numberinput import NumberInput
from widgets.tokeninput import TokenInput
from widgets.sequenceinput import SequenceInput
from data.data import Data
from PyQt5 import QtCore
from models.token_types import Sequence, Token
from models.custom_c_types import C_Token, C_Sequence
from ctypes import cdll, CDLL, c_void_p, c_int, c_float, c_double, POINTER, c_char_p, c_bool, c_char, Structure, Array, _Pointer


class SequenceInputList(QWidget):

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.length = 3

        self.setStyleSheet("""
            SequenceInputList {
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
        self.v_layout.setSpacing(Data.padding_1)

        self.inputs: list[SequenceInput] = []

        self.set_sequence_length(self.length)

    def set_sequence_length(self, new_length: int):
        for input in self.inputs:
            input.setParent(None)
        
        self.length = new_length
        for i in range(self.length):
            sequence_input = SequenceInput(None)
            self.v_layout.addWidget(sequence_input)
            self.inputs.append(sequence_input)
    
    def get_sequence_c(self) -> Array[C_Sequence]:
        sequence_c_p = (C_Sequence * self.length)()
        for i in range(self.length):
            length = self.inputs[i].count
            reward = self.inputs[i].reward
            token_sequence = self.inputs[i].get_sequence_c()
            sequence_c_p[i] = C_Sequence(length, reward, token_sequence, length)
        return sequence_c_p

        

