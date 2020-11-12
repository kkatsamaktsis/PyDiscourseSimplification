class Word:
    def __init__(self, value: str):
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Word):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other
        else:
            return False

    def __add__(self, o):
        return self.value + o

    def __radd__(self, o):
        return o + self.value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
