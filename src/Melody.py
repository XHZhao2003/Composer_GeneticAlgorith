class Melody:
    def __init__(self, notes: list, length=32):
        self.notes = notes
        self.len = length
        self.score = 0     # 适应度
        assert self.len == len(self.notes)
    
