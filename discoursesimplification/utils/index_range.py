class IndexRange:
    def __init__(self, from_idx: int, to_idx: int):
        self.from_idx = from_idx
        self.to_idx = to_idx

    def __str__(self):
        return "(" + str(self.from_idx) + " | " + str(self.to_idx) + ")"

    def __repr__(self):
        return self.__str__()
