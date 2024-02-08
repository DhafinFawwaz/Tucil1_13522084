import sys

from models.cracker import Cracker
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QSizePolicy, QGridLayout, QLabel
from PyQt5 import QtWidgets

from PyQt5 import QtCore
from widgets.nicebutton import NiceButton
from widgets.normaltext import NormalText
from widgets.numberinput import NumberInput
from data.data import Data

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            background-color: #222;
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

        # sequence_amount_input

        


        v_layout.addStretch()

        # def on_button_clicked():
            
            # button.setText(str(Cracker.test()))
            # return

            # buffer_size: int = 7
            # width: int = 6
            # height: int = 6

            # matrix_data = [
            #     ["7A", "55", "E9", "E9", "1C", "55"],
            #     ["55", "7A", "1C", "7A", "E9", "55"],
            #     ["55", "1C", "1C", "55", "E9", "BD"],
            #     ["BD", "1C", "7A", "1C", "55", "BD"],
            #     ["BD", "55", "BD", "7A", "1C", "1C"],
            #     ["1C", "55", "55", "7A", "55", "7A"],
            # ]

            # matrix: list[list[MarkableToken]] = []
            # for i in range(height):
            #     matrix.append([])
            #     for j in range(width):
            #         matrix[i].append(MarkableToken(matrix_data[i][j], False))
            # print(matrix)

            # sequence_length: int = 3
            
            # sequence = [
            #     ["BD", "E9", "1C"],
            #     ["BD", "7A", "BD"],
            #     ["BD", "1C", "BD", "55"],
            # ]
            # # sequence_reward = [15, 20, 30]


            # crack_data = Cracker.getOptimalSolution(buffer_size, width, height, matrix, sequence_length, sequence)

            # print("clicked")
        # button.clicked.connect(on_button_clicked)


if __name__ == "__main__":
    Cracker.initialize()
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())

    