import sys
from time import time
from models.token_types import Token, MarkableToken, Sequence, TokenSlot, CrackData
from models.custom_c_types import C_Token, C_MarkableToken, C_Sequence, C_TokenSlot, C_CrackData
from ctypes import cdll, CDLL, c_void_p, c_int, c_float, c_double, POINTER, c_char_p, c_bool, c_char, Structure

from models.cracker import Cracker
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QSizePolicy, QGridLayout, QLabel
from PyQt5 import QtWidgets

from PyQt5 import QtCore
from widgets.nicebutton import NiceButton
from widgets.normaltext import NormalText
from widgets.numberinput import NumberInput
from widgets.matrixinput import MatrixInput
from data.data import Data

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            background-color: rgb(2, 6, 23);
            color: white;
            font-size: 17px;
            font-weight: bold;
        """)

        self.setWindowTitle(Data.title)
        self.resize(Data.screen_width, Data.screen_height)
        
        v_layout = QVBoxLayout()
        self.setLayout(v_layout)

        title = NormalText(None, Data.title)
        title.setAlignment(QtCore.Qt.AlignCenter)

        v_layout.addWidget(title)

        # buffer_size_input
        buffer_size_h_layout = QHBoxLayout()
        buffer_size_label = NormalText(None, "Buffer Size: ")
        buffer_size_h_layout.addWidget(buffer_size_label)
        buffer_size_input = NumberInput(self, 5)
        buffer_size_h_layout.addWidget(buffer_size_input)
        buffer_size_h_layout.addStretch()
        v_layout.addLayout(buffer_size_h_layout)

        # width, height
        dimension_h_layout = QHBoxLayout()
        dimension_h_layout.setAlignment(QtCore.Qt.AlignLeft)
        width_label = NormalText(None, "Width: ")
        height_label = NormalText(None, "Height: ")
        width_input = NumberInput(self, 5)
        height_input = NumberInput(self, 5)
        dimension_h_layout.addWidget(width_label)
        dimension_h_layout.addWidget(width_input)
        dimension_h_layout.addWidget(height_label)
        dimension_h_layout.addWidget(height_input)
        dimension_h_layout.addStretch()
        v_layout.addLayout(dimension_h_layout)

        # matrix
        matrix_label = NormalText(None, "Tokens: ")
        v_layout.addWidget(matrix_label)
        matrix_h_layout = QHBoxLayout()
        matrix_input = MatrixInput(None, 5, 5)
        matrix_h_layout.addWidget(matrix_input)
        matrix_h_layout.addStretch()
        v_layout.addLayout(matrix_h_layout)

        # sequence_amount_input

        button_h_layout = QHBoxLayout()
        button = NiceButton(None)
        button.setText("Calculate")
        v_layout.addWidget(button)
        button_h_layout.addWidget(button)
        v_layout.addLayout(button_h_layout)

                


        v_layout.addStretch()

        def on_button_clicked():
            
            button.setText(str(Cracker.test()))
            # return

            buffer_size: int = 7
            width: int = 6
            height: int = 6

            matrix_data = [
                ["7A", "55", "E9", "E9", "1C", "55"],
                ["55", "7A", "1C", "7A", "E9", "55"],
                ["55", "1C", "1C", "55", "E9", "BD"],
                ["BD", "1C", "7A", "1C", "55", "BD"],
                ["BD", "55", "BD", "7A", "1C", "1C"],
                ["1C", "55", "55", "7A", "55", "7A"],
            ]
            matrix_data_c_p = (POINTER(C_MarkableToken) * height)()
            for i in range(height):
                matrix_data_c_p[i] = (C_MarkableToken * width)()
                for j in range(width):
                    matrix_data_c_p[i][j] = C_MarkableToken(C_Token(matrix_data[i][j]), False)

            

            sequence = [
                ["BD", "E9", "1C"],
                ["BD", "7A", "BD"],
                ["BD", "1C", "BD", "55"],
            ]
            sequence_length = len(sequence)
            sequence_reward = [15, 20, 30]
            sequence_c_p = (C_Sequence * sequence_length)()
            for i in range(sequence_length):
                length = len(sequence[i])
                token_sequence = (C_Token * length)()
                for j in range(length):
                    token_sequence[j] = C_Token(sequence[i][j])
                sequence_c_p[i] = C_Sequence(length, sequence_reward[i], token_sequence, length)

            start_time = time()
            crack_data_c = Cracker.cracker.getOptimalSolution(
                buffer_size,
                width,
                height,
                matrix_data_c_p,
                sequence_length,
                sequence_c_p
            )
            crack_data = CrackData(crack_data_c)
            print("Execution Time C: ", crack_data.executionDuration, "ms")

            print("max reward", crack_data.maxReward)
            for i in range(crack_data.mostRewardingSlot.bufferSize):
                print(crack_data.mostRewardingSlot.slotList[i].x, crack_data.mostRewardingSlot.slotList[i].y, crack_data.mostRewardingSlot.slotList[i].token.value)

            

        button.clicked.connect(on_button_clicked)


if __name__ == "__main__":
    Cracker.initialize()
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())

    