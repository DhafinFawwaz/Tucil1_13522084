
import os

from ctypes import cdll, CDLL, c_void_p, c_int, c_float, c_double, POINTER, c_char_p, c_bool, c_char, Structure
from models.custom_c_types import C_Token, C_MarkableToken, C_Sequence, C_TokenSlot, C_CrackData
from models.token_types import Token, MarkableToken, Sequence, TokenSlot, CrackData

class Cracker:
    cracker: CDLL = None
    def initialize():
        # get path "../../../lib/cracker.so"
        current_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(current_dir, "..", "..", "lib")
        Cracker.cracker = CDLL(path + "\cracker.so", winmode=0)
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

