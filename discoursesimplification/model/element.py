from discoursesimplification.model.simple_context import SimpleContext
from discoursesimplification.model.linked_context import LinkedContext
from discoursesimplification.utils.ID_generator import IDGenerator
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.words import words_utils


class Element:

    def __init__(self, parse_tree: any, sentence_index: int, context_layer: int):
        self.id = IDGenerator.generate_uuid()
        self.parse_tree = parse_tree
        self.sentence_index = sentence_index
        self.context_layer = context_layer
        self.simple_contexts = []
        self.linked_contexts = []

        self.text = words_utils.words_to_string(parse_tree_extraction_utils.get_containing_words(self.parse_tree))

    def add_linked_context(self, context: LinkedContext):
        if context not in self.linked_contexts:
            self.linked_contexts.append(context)

    def add_simple_context(self, context: SimpleContext):
        if context not in self.simple_contexts:
            self.simple_contexts.append(context)

    def __str__(self):
        res = ""
        res += (str(self.id) + "     " + str(self.context_layer) + "     " + self.text + "\n")

        for c in self.simple_contexts:
            res += ("\tS:" + str(c.relation.value) + "    " + c.text + "\n")
        for c in self.linked_contexts:
            res += ("\tL:" + str(c.relation.value) + "    " + c.target_id + "\n")

        return res
