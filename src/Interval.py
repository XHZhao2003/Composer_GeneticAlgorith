# 用于评分音程的单例
class Interval:
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self):
        # 简化：音程只由半音数确定。在F3-G5范围中可能的音程有27个
        # 根据半音数定义音程的和谐程度，score越低越和谐
        self.interval2score = [
            1.00,           # 纯一度           0
            3.00,           # 小二度           1
            3.00,           # 大二度           2
            2.00,           # 小三度           3
            2.00,           # 大三度           4
            1.00,           # 纯四度           5
            5.00,           # 增四/减五度      6
            1.00,           # 纯五度           7
            2.00,           # 小六度           8
            2.00,           # 大六度           9
            3.00,           # 小七度           10
            3.00,           # 大七度           11
            3.00,           # 纯八度           12
        ] + [5.00] * 14     # 大于八度
    
    def ScoreTwoNote(self, note1 : int, note2 : int):
        if note1 < 2 or note1 > 28:
            raise ValueError("Unexpected note1 %d" % note1)
        if note2 < 2 or note2 > 28:
            raise ValueError("Unexpected note2 %d" % note2)
        interval = abs(note2 - note1)
        return self.interval2score[interval]


