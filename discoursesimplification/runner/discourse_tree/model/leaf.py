from __future__ import annotations

from typing import List

from discoursesimplification.runner.discourse_tree.model.discourse_tree import DiscourseTree
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.parse_tree.parse_tree_parser import ParseTreeParser
from discoursesimplification.utils.pretty_tree_printer import DefaultEdge
from discoursesimplification.utils.words import words_utils


class Leaf(DiscourseTree):

    def __init__(self, extraction_rule: str = None, parse_tree: any = None, text: str = None):
        extraction_rule = "UNKNOWN" if extraction_rule is None else extraction_rule
        super().__init__(extraction_rule)

        if parse_tree is None and text is not None:
            # Generate parse_tree from text
            parse_tree = ParseTreeParser.parse(text)
        if parse_tree is not None and text is None:
            # Generate text from parse_tree
            text = words_utils.words_to_string(parse_tree_extraction_utils.yield_words(parse_tree, []))

        self.text = text
        self.parse_tree = parse_tree
        self.allow_split = True
        self.to_simple_context = False

    def get_core_path_leaves(self) -> List[Leaf]:
        res = [self]

        return res

    def get_previous_node(self) -> DiscourseTree:
        if self.parent is not None:

            # recursion
            return self.parent.get_previous_node()

        return None

    def get_text(self):
        return words_utils.words_to_string(parse_tree_extraction_utils.get_containing_words(self.parse_tree))

    def usable_as_reference(self):
        return (self.parent is not None) \
               and self.parent.is_coordination and self.parent.relation == Relation.UNKNOWN

    # VISUALIZATION
    def get_ptp_caption(self) -> List[str]:
        return ["'" + self.get_text() + "'"]

    def get_ptp_edges(self) -> List[DefaultEdge]:
        return []
