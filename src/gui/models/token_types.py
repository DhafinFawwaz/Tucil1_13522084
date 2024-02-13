
from models.custom_c_types import C_CrackData
class Token():
    def __init__(self, value: str):
        self.value: str = value
    def byteToStr(b: bytes):
        return str(b.decode("utf-8"))

class MarkableToken():
    def __init__(self, token: Token, isMarked: bool):
        self.token: Token = token
        self.isMarked: bool = isMarked

class Sequence():
    def __init__(self, count: int, reward: int, buffer: list[Token]):
        self.count: int = count
        self.reward: int = reward
        self.buffer: list[Token] = buffer

class TokenSlot():
    class TokenSlotData():
        def __init__(self, token: Token, x: int, y: int):
            self.token: Token = token
            self.x: int = x
            self.y: int = y
    def __init__(self, bufferSize: int, filledSlot: int, slotList: list[TokenSlotData]):
        self.bufferSize: int = bufferSize
        self.filledSlot: int = filledSlot
        self.slotList: list[TokenSlot.TokenSlotData] = slotList

class CrackData():
    def __init__(self, mostRewardingSlot: TokenSlot, maxReward: int, executionDuration: int):
        self.mostRewardingSlot: TokenSlot = mostRewardingSlot
        self.maxReward: int = maxReward
        self.executionDuration: int = executionDuration # in ms
    def __init__(self, crack_data: C_CrackData):
        self.maxReward = crack_data.maxReward
        self.executionDuration = crack_data.executionDuration
        self.mostRewardingSlot = TokenSlot(crack_data.mostRewardingSlot.bufferSize, crack_data.mostRewardingSlot.filledSlot, [])
        for i in range(crack_data.mostRewardingSlot.bufferSize):
            temp = crack_data.mostRewardingSlot.slotList[i]
            self.mostRewardingSlot.slotList.append(
                TokenSlot.TokenSlotData(
                    Token(str(temp.token.value.decode("utf-8"))),
                    temp.x,
                    temp.y
                )
            )
       
class TokenMatrix:
    def __init__(self, height: int, width: int):
        self.buffer: list[list[Token]] = [[]]
        self.height: int = height
        self.width: int = width
        for i in range(height):
            for j in range(width):
                self.buffer[i].append(Token("AA"))
            self.buffer.append([])
    
    def set_width(self, new_width: int):
        if new_width < 0:
            return
        if new_width > self.width:
            for i in range(self.height):
                for j in range(new_width - self.width):
                    self.buffer[i].append(Token("AA"))
        else:
            for i in range(self.height):
                for j in range(self.width - new_width):
                    self.buffer[i].pop()
        self.width = new_width

    def set_height(self, new_height: int):
        self.height = new_height
        if new_height < 0:
            return
        if new_height > self.height:
            new_list = []
            for j in range(self.width):
                new_list.append(Token("AA"))
            for i in range(new_height - self.height):
                self.buffer.append(new_list)
        else:
            for i in range(self.height):
                self.buffer.pop()
        self.height = new_height