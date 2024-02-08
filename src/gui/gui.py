import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from widgets.nicebutton import NiceButton
from ctypes import cdll, CDLL, c_void_p, c_int, c_float, c_double, POINTER, c_char_p, c_bool, c_char, Structure
from models.custom_c_types import C_Token, C_MarkableToken, C_Sequence, C_TokenSlot, C_CrackData
from models.token_types import Token, MarkableToken, Sequence, TokenSlot, CrackData

class Cracker:
    cracker: CDLL = None
    def initialize():
        current_dir = os.path.dirname(os.path.realpath(__file__))
        Cracker.cracker = CDLL(current_dir + "\cracker.so", winmode=0)
        Cracker.cracker.getOptimalSolution.argtypes = [c_int, c_int, c_int, POINTER(POINTER(C_MarkableToken)), c_int, POINTER(C_Sequence)]
        Cracker.cracker.getOptimalSolution.restype = C_CrackData
        Cracker.cracker.test.restype = c_int

    def test():
        return Cracker.cracker.test()

    # CrackData getOptimalSolution(int bufferSize, int width, int height, MarkableToken** matrix, int sequenceLength, Sequence sequence[])
    def getOptimalSolution(
        bufferSize: int,
        width: int,
        height: int,
        matrix: POINTER(POINTER(C_MarkableToken)),
        sequence_length: int,
        sequence: POINTER(C_Sequence)
    ) -> C_CrackData:
        return Cracker.cracker.getOptimalSolution(bufferSize, width, height, matrix, sequence_length, sequence)



if __name__ == "__main__":
    Cracker.initialize()

    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(300,300)
    w.setWindowTitle("hmm")
    w.show()

    button = NiceButton(w)
    button.setText("Click me")
    button.setGeometry(50,100,200,50)
    button.show()

    def on_button_clicked():
        
        button.setText(str(Cracker.test()))
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
    button.clicked.connect(on_button_clicked)

    sys.exit(app.exec_())