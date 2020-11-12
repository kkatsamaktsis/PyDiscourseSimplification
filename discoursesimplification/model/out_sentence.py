from discoursesimplification.model.element import Element


class OutSentence:

    def __init__(self, sentence_index: int, original_sentence: str):
        self.sentence_index = sentence_index
        self.original_sentence = original_sentence    
        self.element_dict = {}

    def add_element(self, element: Element):
        if self.sentence_index != element.sentence_index:
            raise AssertionError("ERROR Element should not be added to this sentence")
        self.element_dict[element.id] = element

    def get_element(self, id_input: str):
        return self.element_dict[id_input]

    def get_elements(self):
        return list(self.element_dict.values())

    def __str__(self):
        res = ""
        res += ("# " + self.original_sentence + "\n")
        for e in self.get_elements():
            res += ("\n" + str(e))
        return res
