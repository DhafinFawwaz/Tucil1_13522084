from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5 import QtCore
from widgets.tokeninput import TokenInput
from models.token_types import Token, TokenMatrix
from models.custom_c_types import C_MarkableToken, C_Token
from ctypes import cdll, CDLL, c_void_p, c_int, c_float, c_double, POINTER, c_char_p, c_bool, c_char, Structure, Array, _Pointer


class MatrixInput(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.matrix_height = 5
        self.matrix_width = 7

        spacing = 10

        self.v_layout = QVBoxLayout()
        self.v_layout.setSpacing(spacing)
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.v_layout)

        self.inputs: list[TokenInput] = []
        self.set_width(self.matrix_width)


    def get_matrix(self):
        matrix = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                s: str = self.inputs[i*self.matrix_width+j].text()
                row.append(s)
            matrix.append(row)
        return matrix
    
    def get_matrix_c(self): #  -> Array[_Pointer[C_MarkableToken]]
        matrix_data_c_p = (POINTER(C_MarkableToken) * self.matrix_height)()
        for i in range(self.matrix_height):
            matrix_data_c_p[i] = (C_MarkableToken * self.matrix_width)()
            for j in range(self.matrix_width):
                token_str = self.inputs[i*self.matrix_width+j].text()
                matrix_data_c_p[i][j] = C_MarkableToken(C_Token(token_str), False)
        return matrix_data_c_p
    
    def set_width(self, new_width: int):
        for input in self.inputs:
            input.setParent(None)
        
        self.matrix_width = new_width

        self.inputs: list[TokenInput] = []
        spacing = 10
        for i in range(self.matrix_height):
            h_layout = QHBoxLayout()
            h_layout.setSpacing(spacing)
            for j in range(self.matrix_width):
                token_input = TokenInput(self, 0)
                h_layout.addWidget(token_input)
                self.inputs.append(token_input)
            h_layout.addStretch()
            self.v_layout.addLayout(h_layout)
        
    def set_height(self, new_height: int):
        for input in self.inputs:
            input.setParent(None)
        
        self.matrix_height = new_height

        self.inputs: list[TokenInput] = []
        spacing = 10
        for i in range(self.matrix_height):
            h_layout = QHBoxLayout()
            h_layout.setSpacing(spacing)
            for j in range(self.matrix_width):
                token_input = TokenInput(self, 0)
                h_layout.addWidget(token_input)
                self.inputs.append(token_input)
            h_layout.addStretch()
            self.v_layout.addLayout(h_layout)