from __future__ import annotations

from typing import List

from discoursesimplification.runner.discourse_tree.model.coordination import Coordination
from discoursesimplification.runner.discourse_tree.model.discourse_tree import DiscourseTree
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf
from discoursesimplification.utils.pretty_tree_printer import DefaultEdge


class Subordination(DiscourseTree):

    def __init__(self, extraction_rule: str, relation: Relation, cue_phrase: str, left_constituent: DiscourseTree,
                 right_constituent: DiscourseTree, context_right: bool):
        super().__init__(extraction_rule)
        self.relation = relation
        self.cue_phrase = cue_phrase
        self.context_right = context_right

        self.left_constituent = Leaf()  # temp
        self.right_constituent = Leaf()  # temp
        self.replace_left_constituent(left_constituent)
        self.replace_right_constituent(right_constituent)

    def set_recursive_unset_sentence_index(self, sentence_index: int):
        if self.sentence_index < 0:
            self.sentence_index = sentence_index

            # recursive
            self.left_constituent.set_recursive_unset_sentence_index(sentence_index)
            self.right_constituent.set_recursive_unset_sentence_index(sentence_index)

    def clean_up(self):
        # recursion
        self.left_constituent.clean_up()
        self.right_constituent.clean_up()

    def usable_as_reference(self):
        return (self.parent is not None) \
               and isinstance(self.parent, Coordination) and self.parent.relation == Relation.UNKNOWN

    def get_core_path_leaves(self) -> List[Leaf]:
        res = []

        # recursion on superordinations
        res.extend(self.get_superordination().get_core_path_leaves())

        return res

    def parent_get_previous_node(self) -> DiscourseTree:
        if self.right_constituent == self:
            return self.left_constituent
        return None

    def replace_left_constituent(self, new_left_constituent):
        old_left_constituent = self.left_constituent
        self.left_constituent = new_left_constituent
        new_left_constituent.parent = self
        new_left_constituent.set_recursive_unset_sentence_index(old_left_constituent.sentence_index)

    def replace_right_constituent(self, new_right_constituent):
        old_right_constituent = self.right_constituent
        self.right_constituent = new_right_constituent
        new_right_constituent.parent = self
        new_right_constituent.set_recursive_unset_sentence_index(old_right_constituent.sentence_index)

    def replace_superordination(self, new_superordination):
        if self.context_right:
            self.replace_left_constituent(new_superordination)
        else:
            self.replace_right_constituent(new_superordination)

    def replace_subordination(self, new_subordination):
        if self.context_right:
            self.replace_right_constituent(new_subordination)
        else:
            self.replace_left_constituent(new_subordination)

    def get_superordination(self):
        if self.context_right:
            return self.left_constituent
        else:
            return self.right_constituent

    def get_subordination(self):
        if self.context_right:
            return self.right_constituent
        else:
            return self.left_constituent

    # VISUALIZATION
    def get_ptp_caption(self) -> List[str]:
        cue_phrase_str = "'" + self.cue_phrase + "'" if self.cue_phrase is not None else "NULL"
        return ["SUB/" + str(self.relation.value) + " (" + cue_phrase_str + ", " + self.extraction_rule + ")"]

    def get_ptp_edges(self) -> List[DefaultEdge]:
        res = [DefaultEdge("n" if self.context_right else "s", self.left_constituent, True),
               DefaultEdge("s" if self.context_right else "n", self.right_constituent, True)]

        return res
