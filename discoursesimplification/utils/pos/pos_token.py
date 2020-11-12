class POSToken:
    def __init__(self, index: int, text: str, pos: str):
        self.index = index
        self.text = text
        self.pos = pos

    def __str__(self):
        return "(" + str(self.index) + ": " + self.pos + ", '" + self.text + "')"

    # This method is called by lists for the str representation of each element.
    def __repr__(self):
        return self.__str__()
