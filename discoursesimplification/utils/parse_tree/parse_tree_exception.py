class ParseTreeException(Exception):

    def __init__(self, text: str):
        self.message = "Failed to parse text: \"" + text + "\""

    def __str__(self):
        return repr(self.message)
