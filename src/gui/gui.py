import sys
from time import time
from models.token_types import Token, MarkableToken, Sequence, TokenSlot, CrackData
from models.custom_c_types import C_Token, C_MarkableToken, C_Sequence, C_TokenSlot, C_CrackData
from ctypes import cdll, CDLL, c_void_p, c_int, c_float, c_double, POINTER, c_char_p, c_bool, c_char, Structure

from models.cracker import Cracker
from models.token_types import TokenMatrix
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QSizePolicy, QGridLayout, QLabel
from PyQt5 import QtWidgets

from PyQt5 import QtCore
from widgets.nicebutton import NiceButton
from widgets.normaltext import NormalText
from widgets.numberinput import NumberInput
from widgets.matrixinput import MatrixInput
from widgets.sequenceinput import SequenceInput
from widgets.vcontainer import VContainer
from widgets.sequenceinputlist import SequenceInputList
from data.data import Data


class Window(QWidget):
    
    def on_buffer_size_changed(self, text: str):
        if text.isdigit():
            val = int(text)
            if val < 1:
                return
            self.buffer_size = val
    
    def on_width_changed(self, text: str):
        if text.isdigit():
            val = int(text)
            if val < 1:
                return
            self.matrix_input.set_width(val)
    
    def on_height_changed(self, text: str):
        if text.isdigit():
            val = int(text)
            if val < 1:
                return
            self.matrix_input.set_height(val)

    def on_sequence_amount_changed(self, text: str):
        if text.isdigit():
            val = int(text)
            if val < 1:
                return 
            self.sequence_input_list.set_sequence_length(val)

    def __init__(self):
        super().__init__()
        self.buffer_size: int = 5
        self.sequence_amount: int = 3


        self.setStyleSheet("""
            background-color: rgb(2, 6, 23);
            color: white;
            font-size: 17px;
            font-weight: bold;
        """)

        self.setWindowTitle(Data.title)
        self.resize(Data.screen_width, Data.screen_height)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(Data.padding_2)
        self.setLayout(grid_layout)
        
        v_layout_left = QVBoxLayout()
        v_layout_left.setSpacing(Data.padding_1)
        v_layout_right = QVBoxLayout()
        v_layout_right.setSpacing(Data.padding_1)
        grid_layout.addLayout(v_layout_left, 1, 0)
        grid_layout.addLayout(v_layout_right, 1, 1)

        # title
        title = NormalText(None, Data.title)
        title.setStyleSheet("QLabel{font-size: 24px;}")
        title.setAlignment(QtCore.Qt.AlignCenter)     
        grid_layout.addWidget(title, 0, 0, 1, 0)
        
        
        # input title
        input_title = NormalText(None, "Input:")
        v_layout_left.addWidget(input_title)
        input_title.setAlignment(QtCore.Qt.AlignLeft)        
        input_title.setMinimumWidth(Data.screen_width//2)      

        # result title
        result_title = NormalText(None, "Result:")
        v_layout_right.addWidget(result_title)
        result_title.setAlignment(QtCore.Qt.AlignLeft)  
        result_title.setMinimumWidth(Data.screen_width//2)      


        buffer_size_hcontainer = VContainer()

        # buffer_size_input
        buffer_size_layout = QHBoxLayout()
        buffer_size_label = NormalText(None, "Buffer Size: ")
        buffer_size_input = NumberInput(self, 5)
        buffer_size_input.set_allow_negative(False)
        buffer_size_input.setText(str(self.buffer_size))
        buffer_size_input.setFixedWidth(Data.input_width_2)
        buffer_size_layout.addWidget(buffer_size_label)
        buffer_size_layout.addWidget(buffer_size_input)
        buffer_size_layout.addStretch()
        buffer_size_hcontainer.addLayout(buffer_size_layout)
        v_layout_left.addWidget(buffer_size_hcontainer)
        buffer_size_input.textChanged.connect(self.on_buffer_size_changed)


        dimension_hcontainer = VContainer()

        # width, height
        dimension_h_layout = QHBoxLayout()
        dimension_h_layout.setAlignment(QtCore.Qt.AlignLeft)
        width_label = NormalText(None, "Width: ")
        height_label = NormalText(None, "Height: ")
        width_input = NumberInput(self, 5)
        height_input = NumberInput(self, 5)
        width_input.set_allow_negative(False)
        height_input.set_allow_negative(False)
        width_input.setMaximumWidth(Data.input_width_1)
        height_input.setMaximumWidth(Data.input_width_1)
        dimension_h_layout.addWidget(width_label)
        dimension_h_layout.addWidget(width_input)
        dimension_h_layout.addWidget(height_label)
        dimension_h_layout.addWidget(height_input)
        dimension_h_layout.addStretch()
        dimension_hcontainer.addLayout(dimension_h_layout)

        # matrix
        matrix_label = NormalText(None, "Tokens: ")
        dimension_hcontainer.addWidget(matrix_label)
        matrix_h_layout = QHBoxLayout()
        
        self.matrix_input = MatrixInput(None)
        width_input.setText(str(self.matrix_input.matrix_width))
        height_input.setText(str(self.matrix_input.matrix_height))
        width_input.textChanged.connect(self.on_width_changed)
        height_input.textChanged.connect(self.on_height_changed)

        matrix_h_layout.addWidget(self.matrix_input)
        matrix_h_layout.addStretch()
        dimension_hcontainer.addLayout(matrix_h_layout)

        v_layout_left.addWidget(dimension_hcontainer)


        sequence_hcontainer = VContainer()
        
        # sequence_amount_input
        h_layout_sequence = QHBoxLayout()
        sequence_label = NormalText(None, "Amount of Sequence: ")
        sequence_amount_input = NumberInput(None, 0)
        sequence_amount_input.set_allow_negative(False)
        sequence_amount_input.setFixedWidth(Data.input_width_1+7)
        sequence_amount_input.setText(str(self.sequence_amount))
        sequence_amount_input.textChanged.connect(self.on_sequence_amount_changed)
        h_layout_sequence.addWidget(sequence_label)
        h_layout_sequence.addWidget(sequence_amount_input)
        h_layout_sequence.addStretch()
        sequence_hcontainer.addLayout(h_layout_sequence)
        v_layout_left.addWidget(sequence_hcontainer)

        self.h_layout_sequence_list = QHBoxLayout()

        self.sequence_input_list = SequenceInputList(None)
        self.sequence_input_list.set_sequence_length(self.sequence_amount)
        v_layout_left.addWidget(self.sequence_input_list)



        # button
        button_h_layout = QHBoxLayout()
        calculate_button = NiceButton(None)
        calculate_button.setText("Auto Generate Values")
        v_layout_left.addWidget(calculate_button)
        button_h_layout.addWidget(calculate_button)
        calculate_button = NiceButton(None)
        calculate_button.setText("Import Values from File")
        v_layout_left.addWidget(calculate_button)
        button_h_layout.addWidget(calculate_button)
        v_layout_left.addLayout(button_h_layout)
        button_h_layout.setSpacing(Data.padding_1)
        # button_h_layout.addStretch()


        button_h_layout = QHBoxLayout()
        calculate_button = NiceButton(None)
        calculate_button.setText("Calculate")
        button_h_layout.addWidget(calculate_button)
        v_layout_left.addLayout(button_h_layout)
        # button_h_layout.addStretch()
        

                



        def on_button_clicked():
            
            buffer_size: int = self.buffer_size
            width: int = self.matrix_input.matrix_width
            height: int = self.matrix_input.matrix_height

            matrix_data_c_p = self.matrix_input.get_matrix_c()

            sequence_c_p = self.sequence_input_list.get_sequence_c()

            crack_data_c = Cracker.cracker.getOptimalSolution(
                buffer_size,
                width,
                height,
                matrix_data_c_p,
                self.sequence_amount,
                sequence_c_p
            )
            crack_data = CrackData(crack_data_c)
            print("Execution Time C: ", crack_data.executionDuration, "ms")

            print("max reward", crack_data.maxReward)
            for i in range(crack_data.mostRewardingSlot.bufferSize):
                print(crack_data.mostRewardingSlot.slotList[i].x, crack_data.mostRewardingSlot.slotList[i].y, crack_data.mostRewardingSlot.slotList[i].token.value)

            

        calculate_button.clicked.connect(on_button_clicked)


        

        v_layout_left.addStretch()
        v_layout_right.addStretch()



if __name__ == "__main__":
    Cracker.initialize()
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())

    