import sys
from time import time

from PyQt5.QtGui import QResizeEvent
from models.token_types import Token, MarkableToken, Sequence, TokenSlot, CrackData
from models.custom_c_types import C_Token, C_MarkableToken, C_Sequence, C_TokenSlot, C_CrackData
from ctypes import cdll, CDLL, c_void_p, c_int, c_float, c_double, POINTER, c_char_p, c_bool, c_char, Structure, _Pointer, Array

from models.cracker import Cracker
from models.token_types import TokenMatrix
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QSizePolicy, QGridLayout, QLabel, QFileDialog, QScrollArea
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
import os

class Window(QWidget):
    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self.scrollArea.setFixedWidth(self.width())
        self.scrollArea.setFixedHeight(self.height())
        return super().resizeEvent(a0)
    
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
        self.sequence_amount: int = 2


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
        
        
        self.v_layout_left = QVBoxLayout()
        self.v_layout_left.setSpacing(Data.padding_1)
        self.v_layout_right = QVBoxLayout()
        self.v_layout_right.setSpacing(Data.padding_1)
        grid_layout.addLayout(self.v_layout_left, 1, 0)
        grid_layout.addLayout(self.v_layout_right, 1, 1)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setRowStretch(1, 1)

        # Make the v_layout_left scrollable without shrinking
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMinimumHeight(Data.screen_height)
        self.scrollArea.setMinimumWidth(Data.screen_width)

        widget = QWidget()
        self.scrollArea.setWidget(widget)
        widget.setLayout(grid_layout)
        # make scroll area size always adjust according to window size
        self.scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scrollArea.setWidgetResizable(True)
        


        # title
        title = NormalText(None, Data.title)
        title.setStyleSheet("QLabel{font-size: 24px;}")
        title.setAlignment(QtCore.Qt.AlignCenter)     
        grid_layout.addWidget(title, 0, 0, 1, 0)
        
        
        # input title
        input_title = NormalText(None, "Input:")
        self.v_layout_left.addWidget(input_title)
        input_title.setAlignment(QtCore.Qt.AlignLeft)        
        input_title.setMinimumWidth(Data.screen_width//2)      

        # result title
        result_title = NormalText(None, "Result:")
        self.v_layout_right.addWidget(result_title)
        result_title.setAlignment(QtCore.Qt.AlignLeft)  
        result_title.setMinimumWidth(Data.screen_width//2)      


        buffer_size_hcontainer = VContainer()

        # buffer_size_input
        buffer_size_layout = QHBoxLayout()
        buffer_size_label = NormalText(None, "Buffer Size: ")
        self.buffer_size_input = NumberInput(self, 5)
        self.buffer_size_input.set_allow_negative_or_zero(False)
        self.buffer_size_input.setText(str(self.buffer_size))
        self.buffer_size_input.setFixedWidth(Data.input_width_2)
        buffer_size_layout.addWidget(buffer_size_label)
        buffer_size_layout.addWidget(self.buffer_size_input)
        buffer_size_layout.addStretch()
        buffer_size_hcontainer.addLayout(buffer_size_layout)
        self.v_layout_left.addWidget(buffer_size_hcontainer)
        self.buffer_size_input.textChanged.connect(self.on_buffer_size_changed)


        dimension_hcontainer = VContainer()

        # width, height
        dimension_h_layout = QHBoxLayout()
        dimension_h_layout.setAlignment(QtCore.Qt.AlignLeft)
        width_label = NormalText(None, "Width: ")
        height_label = NormalText(None, "Height: ")
        self.width_input = NumberInput(self, 5)
        self.height_input = NumberInput(self, 5)
        self.width_input.set_allow_negative_or_zero(False)
        self.height_input.set_allow_negative_or_zero(False)
        self.width_input.setMaximumWidth(Data.input_width_1)
        self.height_input.setMaximumWidth(Data.input_width_1)
        dimension_h_layout.addWidget(width_label)
        dimension_h_layout.addWidget(self.width_input)
        dimension_h_layout.addWidget(height_label)
        dimension_h_layout.addWidget(self.height_input)
        dimension_h_layout.addStretch()
        dimension_hcontainer.addLayout(dimension_h_layout)

        # matrix
        matrix_label = NormalText(None, "Tokens: ")
        dimension_hcontainer.addWidget(matrix_label)
        matrix_h_layout = QHBoxLayout()
        
        self.matrix_input = MatrixInput(None)
        self.width_input.setText(str(self.matrix_input.matrix_width))
        self.height_input.setText(str(self.matrix_input.matrix_height))
        self.width_input.textChanged.connect(self.on_width_changed)
        self.height_input.textChanged.connect(self.on_height_changed)

        matrix_h_layout.addWidget(self.matrix_input)
        matrix_h_layout.addStretch()
        dimension_hcontainer.addLayout(matrix_h_layout)

        self.v_layout_left.addWidget(dimension_hcontainer)


        sequence_hcontainer = VContainer()
        
        # sequence_amount_input
        h_layout_sequence = QHBoxLayout()
        sequence_label = NormalText(None, "Amount of Sequence: ")
        self.sequence_amount_input = NumberInput(None, 0)
        self.sequence_amount_input.set_allow_negative_or_zero(False)
        self.sequence_amount_input.setFixedWidth(Data.input_width_1+7)
        self.sequence_amount_input.setText(str(self.sequence_amount))
        self.sequence_amount_input.textChanged.connect(self.on_sequence_amount_changed)
        h_layout_sequence.addWidget(sequence_label)
        h_layout_sequence.addWidget(self.sequence_amount_input)
        h_layout_sequence.addStretch()
        sequence_hcontainer.addLayout(h_layout_sequence)
        self.v_layout_left.addWidget(sequence_hcontainer)

        self.h_layout_sequence_list = QHBoxLayout()

        self.sequence_input_list = SequenceInputList(None)
        self.sequence_input_list.set_sequence_length(self.sequence_amount)
        self.v_layout_left.addWidget(self.sequence_input_list)


        self.v_layout_left.addStretch()

        # button
        button_h_layout = QHBoxLayout()
        self.calculate_button = NiceButton(None)
        self.calculate_button.setText("Auto Generate Values")
        self.calculate_button.clicked.connect(self.on_auto_generate_clicked)
        self.v_layout_left.addWidget(self.calculate_button)
        button_h_layout.addWidget(self.calculate_button)
        self.calculate_button = NiceButton(None)
        self.calculate_button.setText("Import Values from File")
        self.calculate_button.clicked.connect(self.on_file_open_clicked)
        self.v_layout_left.addWidget(self.calculate_button)
        button_h_layout.addWidget(self.calculate_button)
        self.v_layout_left.addLayout(button_h_layout)
        button_h_layout.setSpacing(Data.padding_1)
        # button_h_layout.addStretch()


        button_h_layout = QHBoxLayout()
        self.calculate_button = NiceButton(None)
        self.calculate_button.setText("Calculate")
        button_h_layout.addWidget(self.calculate_button)
        self.v_layout_left.addLayout(button_h_layout)
        self.calculate_button.clicked.connect(self.on_calculate_clicked)

        # Result
        self.execution_time_label = NormalText(None, "")
        self.max_reward_label = NormalText(None, "")
        self.v_layout_right.addWidget(self.execution_time_label)
        self.v_layout_right.addWidget(self.max_reward_label)
        
        self.matrix_result_label: list[NormalText] = []

        self.v_layout_right.addStretch()

        self.crack_data: CrackData = None
        self.matrix_c_p: Array[_Pointer[C_MarkableToken]] = None

        self.button_h_layout: QHBoxLayout = None

    def validate_input(self) -> bool:
        # buffer size > 0
        # width > 0
        # height > 0
        # sequence amount > 0
        # count > 0

        # matrix is all filled with 2 character
        # token is all filled with 2 character

        self.execution_time_label.setText("Error: ") # Error message
        self.execution_time_label.set_error_style()
        return True

    def on_calculate_clicked(self):
        if not self.validate_input():
            return
        
        self.execution_time_label.set_default_style()
        self.calculate_button.setText("Processing...")
        self.calculate_button.setEnabled(False)


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
        self.draw_result(crack_data, matrix_data_c_p)

        self.calculate_button.setText("Calculate")
        self.calculate_button.setEnabled(True)

        self.crack_data = crack_data
        self.matrix_c_p = matrix_data_c_p

    def draw_result(self, crack_data: CrackData, matrix_data_c_p):
        # remove all label
        for i in self.matrix_result_label:
            i.setParent(None)
        self.matrix_result_label = []


        self.execution_time_label.setText("Execution Time: " + str(crack_data.executionDuration) + "ms")
        self.max_reward_label.setText("Max Reward: " + str(crack_data.maxReward))

        initX = self.max_reward_label.x()
        initY = self.max_reward_label.y() + 25
        
        delt = 25
        marginX = 20
        marginY = 15


        for i in range(self.matrix_input.matrix_height):
            for j in range(self.matrix_input.matrix_width):
                label = NormalText(self, Token.byteToStr(matrix_data_c_p[i][j].token.value))
                label.move(initX + j*(delt+marginX), initY + i*(delt+marginY))
                label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 14px;
                        font-weight: bold;
                        background-color: rgb(30, 41, 59);
                        max-width: 25px;
                        border-radius: 10px;
                        padding: 5px;
                    }
                """)
                label.show()
                self.matrix_result_label.append(label)

        # draw lines between marks
        line_width = 10
        for i in range(crack_data.mostRewardingSlot.bufferSize-1):
            x1 = crack_data.mostRewardingSlot.slotList[i].x
            y1 = crack_data.mostRewardingSlot.slotList[i].y
            x2 = crack_data.mostRewardingSlot.slotList[i+1].x
            y2 = crack_data.mostRewardingSlot.slotList[i+1].y
            label = NormalText(self, "")

            # swap because negative line width is not supported
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1

            line_draw_deltX = 12
            line_draw_deltY = 10
            if x1 == x2:
                label.setGeometry(initX + x1*(delt+marginX) + line_draw_deltX, initY + y1*(delt+marginY) + line_draw_deltY, line_width, (y2-y1)*(delt+marginY))
            elif y1 == y2:
                label.setGeometry(initX + x1*(delt+marginX) + line_draw_deltX, initY + y1*(delt+marginY) + line_draw_deltY, (x2-x1)*(delt+marginX), line_width)

            label.setStyleSheet("""
                QLabel{
                    background-color: rgb(203, 213, 225);
                }
            """)
            label.show()
            self.matrix_result_label.append(label)

        # draw marked token
        for i in range(crack_data.mostRewardingSlot.bufferSize):
            x = crack_data.mostRewardingSlot.slotList[i].x
            y = crack_data.mostRewardingSlot.slotList[i].y
            label = NormalText(self, Token.byteToStr(matrix_data_c_p[y][x].token.value))
            label.move(initX + x*(delt+marginX), initY + y*(delt+marginY))
            label.setStyleSheet("""
                QLabel{
                    background-color: rgb(203, 213, 225);
                    color: rgb(2, 6, 23); 
                    font-size: 14px;
                    font-weight: bold;
                    max-width: 25px;
                    border-radius: 10px;
                    padding: 5px;
                }
            """)
            label.show()
            self.matrix_result_label.append(label)

        initY = initY + self.matrix_input.matrix_height*(delt+marginY)
        for i in range(crack_data.mostRewardingSlot.bufferSize):
            x = crack_data.mostRewardingSlot.slotList[i].x
            y = crack_data.mostRewardingSlot.slotList[i].y
            label = NormalText(self, "(" + str(x+1) + ", " + str(y+1) + ")")
            label.move(initX, initY + i*25)
            label.setStyleSheet("""
                QLabel{
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
            label.show()
            self.matrix_result_label.append(label)

            self.draw_save_button()
        

    
    def draw_save_button(self):
        if self.button_h_layout is not None:
            for i in range(self.button_h_layout.count()):
                self.button_h_layout.itemAt(i).widget().setParent(None)
            self.v_layout_right.removeItem(self.button_h_layout)

        self.button_h_layout = QHBoxLayout()
        self.save_result_button = NiceButton(None)
        self.save_result_button.setText("Save Result to File")
        self.save_result_button.clicked.connect(self.on_save_result_clicked)
        self.button_h_layout.addWidget(self.save_result_button)
        self.v_layout_right.addLayout(self.button_h_layout)

    def on_file_open_clicked(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        fname = QFileDialog.getOpenFileName(self, 'Open file', current_path, "Text files (*.txt)")

        if fname[0]:
            with open(fname[0], 'r') as f:
                lines = f.readlines()
                if len(lines) < 3:
                    return
                self.buffer_size = int(lines[0])
                self.buffer_size_input.setText(str(self.buffer_size))

                # 6 6
                # split by space
                dimension = lines[1].split(" ")
                width = int(dimension[0])
                height = int(dimension[1])
                self.width_input.setText(str(width))
                self.height_input.setText(str(height))
                self.matrix_input.set_width(width)
                self.matrix_input.set_height(height)

                for i in range(height): # height
                    splitted = lines[i+2].split(" ")
                    for j in range(width):
                        current_input = self.matrix_input.inputs[i*width + j]
                        current_input.setText(splitted[j][:2])

                self.sequence_amount = int(lines[2 + height])
                self.sequence_input_list.set_sequence_length(self.sequence_amount)
                self.sequence_amount_input.setText(str(self.sequence_amount))

                for i in range(0, self.sequence_amount):
                    # input -> i
                    # lines -> i*2
                    splitted = lines[2 + height + 1 + i*2].split(" ")
                    length = len(splitted)
                    self.sequence_input_list.inputs[i].count = length
                    self.sequence_input_list.inputs[i].count_input.setText(str(length))
                    for j in range(0, length):
                        current_input = self.sequence_input_list.inputs[i].inputs[j]
                        current_input.setText(splitted[j][:2])
                    reward = int(lines[2 + height + 1 + i*2 + 1])
                    self.sequence_input_list.inputs[i].reward_input.setText(str(reward))
                    self.sequence_input_list.inputs[i].reward = reward

    def on_auto_generate_clicked(self):
        pass
            
    def on_save_result_clicked(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        fname = QFileDialog.getSaveFileName(self, 'Save file', current_path, "Text files (*.txt)")


        if fname[0]:
            with open(fname[0], 'w') as f:
            # format
            # 50
            # 7A BD 7A BD 1C BD 55 
            # 1, 1
            # 1, 4
            # 3, 4
            # 3, 5
            # 6, 5
            # 6, 3
            # 1, 3

            # 0 ms
                f.write(str(self.crack_data.maxReward) + "\n")
                for i in range(self.crack_data.mostRewardingSlot.bufferSize):
                    x = self.crack_data.mostRewardingSlot.slotList[i].x
                    y = self.crack_data.mostRewardingSlot.slotList[i].y
                    f.write(self.crack_data.mostRewardingSlot.slotList[i].token.value + " ")
                f.write("\n")
                for i in range(self.crack_data.mostRewardingSlot.bufferSize):
                    x = self.crack_data.mostRewardingSlot.slotList[i].x
                    y = self.crack_data.mostRewardingSlot.slotList[i].y
                    f.write(str(x+1) + ", " + str(y+1) + "\n")
                f.write("\n")
                f.write(str(self.crack_data.executionDuration) + "ms\n")


if __name__ == "__main__":
    Cracker.initialize()
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())

    