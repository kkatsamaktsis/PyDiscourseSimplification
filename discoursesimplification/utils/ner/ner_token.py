class NERToken:
    def __init__(self, index: int, text: str, category: str):
        self.index = index
        self.text = text
        self.category = category

    def __str__(self):
        return "(" + str(self.index) + ": " + self.category + ", '" + self.text + "')"

    def __repr__(self):
        return self.__str__()
