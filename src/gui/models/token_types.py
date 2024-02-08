
class Token():
    value: str
    def __init__(self, value: str):
        self.value = value

class MarkableToken():
    token: Token
    isMarked: bool
    def __init__(self, token: Token, isMarked: bool):
        self.token = token
        self.isMarked = isMarked

class Sequence():
    count: int
    reward: int
    buffer: list[Token]
    def __init__(self, count: int, reward: int, buffer: list[Token]):
        self.count = count
        self.reward = reward
        self.buffer = buffer

class TokenSlot():
    class TokenSlotData():
        token: Token
        x: int
        y: int
        def __init__(self, token: Token, x: int, y: int):
            self.token = token
            self.x = x
            self.y = y
    bufferSize: int
    slotList: list[TokenSlotData]
    def __init__(self, bufferSize: int, slotList: list[TokenSlotData]):
        self.bufferSize = bufferSize
        self.slotList = slotList

class CrackData():
    mostRewardingSlot: Token
    maxReward: int
    executionDuration: int # in ms
    def __init__(self, mostRewardingSlot: Token, maxReward: int, executionDuration: int):
        self.mostRewardingSlot = mostRewardingSlot
        self.maxReward = maxReward
        self.executionDuration = executionDuration

       