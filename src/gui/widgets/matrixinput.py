from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5 import QtCore
from widgets.tokeninput import TokenInput

class MatrixInput(QWidget):
    def __init__(self, parent: QWidget, row: int, column: int):
        super().__init__(parent)
        self.row = row
        self.column = column

        spacing = 10

        self.v_layout = QVBoxLayout()
        self.v_layout.setSpacing(spacing)
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.v_layout)
        
        self.inputs = []
        for i in range(row):
            h_layout = QHBoxLayout()
            h_layout.setSpacing(spacing)
            for j in range(column):
                token_input = TokenInput(self, 0)
                h_layout.addWidget(token_input)
                self.inputs.append(token_input)
            h_layout.addStretch()
            self.v_layout.addLayout(h_layout)


        


    def get_matrix(self):
        matrix = []
        for i in range(self.row):
            row = []
            for j in range(self.column):
                row.append(float(self.inputs[i*self.column+j].text()))
            matrix.append(row)
        return matrix