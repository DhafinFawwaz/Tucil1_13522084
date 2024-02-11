
from ctypes import cdll, CDLL, c_void_p, c_int, c_float, c_double, POINTER, c_char_p, c_bool, c_char, Structure
class C_Token(Structure):
    _fields_ = [
        ("value", c_char * 2)
    ]
    def __init__(self, value: str):
        self.value = value.encode('utf-8')

class C_MarkableToken(Structure):
    _fields_ = [
        ("token", C_Token),
        ("isMarked", c_bool)
    ]
class C_Sequence(Structure):
    _fields_ = [
        ("count", c_int),
        ("reward", c_int),
        ("buffer", POINTER(C_Token)),
        ("bufferSize", c_int)
    ]
    def __init__(self, count: int, reward: int, buffer: list[C_Token], bufferSize: int):
        self.count = count
        self.reward = reward
        self.buffer = buffer
        self.bufferSize = bufferSize



class C_TokenSlot(Structure):
    class C_TokenSlotData(Structure):
        _fields_ = [
            ("token", C_Token),
            ("x", c_int),
            ("y", c_int)
        ]
    _fields_ = [
        ("bufferSize", c_int),
        ("slotList", POINTER(C_TokenSlotData))
    ]

class C_CrackData(Structure):
    _fields_ = [
        ("mostRewardingSlot", C_TokenSlot),
        ("maxReward", c_int),
        ("executionDuration", c_int)
    ]

        
    # CrackData getOptimalSolution(int bufferSize, int width, int height, MarkableToken** matrix, int sequenceLength, Sequence sequence[])
    # struct Token{
    #     char value[2];
    # }
    # struct MarkableToken{
    #     Token token;
    #     bool isMarked;
    # };
        
    # struct Sequence{
    #     int count;
    #     int reward;
    #     vector<Token> buffer;
    # };

    # struct CrackData{
    #     TokenSlot mostRewardingSlot;
    #     int maxReward;
    #     int executionDuration;
    # };
        
    # struct TokenSlot{
    #     struct TokenSlotData{
    #         Token token;
    #         int x;
    #         int y;
    #     };

    #     int bufferSize;
    #     TokenSlotData* slotList;
    # }
    
        