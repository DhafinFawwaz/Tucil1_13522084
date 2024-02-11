
from models.custom_c_types import C_CrackData
class Token():
    def __init__(self, value: str):
        self.value: str = value

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
    def __init__(self, bufferSize: int, slotList: list[TokenSlotData]):
        self.bufferSize: int = bufferSize
        self.slotList: list[TokenSlot.TokenSlotData] = slotList

class CrackData():
    def __init__(self, mostRewardingSlot: TokenSlot, maxReward: int, executionDuration: int):
        self.mostRewardingSlot: TokenSlot = mostRewardingSlot
        self.maxReward: int = maxReward
        self.executionDuration: int = executionDuration # in ms
    def __init__(self, crack_data: C_CrackData):
        self.maxReward = crack_data.maxReward
        self.executionDuration = crack_data.executionDuration
        self.mostRewardingSlot = TokenSlot(crack_data.mostRewardingSlot.bufferSize, [])
        for i in range(crack_data.mostRewardingSlot.bufferSize):
            temp = crack_data.mostRewardingSlot.slotList[i]
            self.mostRewardingSlot.slotList.append(
                TokenSlot.TokenSlotData(
                    Token(str(temp.token.value.decode("utf-8"))),
                    temp.x,
                    temp.y
                )
            )
       