from __future__ import annotations

from discoursesimplification.utils.ner.ner_token import NERToken
from discoursesimplification.utils import tree_utils


class TNERToken(NERToken):
    def __init__(self, index: int, token: str, category: str, leaf_node):
        super().__init__(index, token, category)
        self.ner_string = None
        self.leaf_node = leaf_node
        self.pos_node = None  # wait until ner_string is set

    def set_ner_string(self, ner_string):
        self.ner_string = ner_string
        self.pos_node = tree_utils.parent(self.leaf_node, self.get_parse_tree())

    def get_parse_tree(self):
        return self.ner_string.parse_tree

    def get_pos_tag(self):
        return self.pos_node.value

    def __str__(self):
        return "(" + str(self.index) + ": " + self.category + ", '" + self.text + "', " + self.get_pos_tag() + "')"

    def __repr__(self):
        return self.__str__()
