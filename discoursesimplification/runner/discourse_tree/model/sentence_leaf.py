from discoursesimplification.runner.discourse_tree.model.leaf import Leaf


class SentenceLeaf(Leaf):

    def __init__(self, sentence: str, sentence_index: int):
        super().__init__("SENTENCE", None, sentence)
        self.set_recursive_unset_sentence_index(sentence_index)
