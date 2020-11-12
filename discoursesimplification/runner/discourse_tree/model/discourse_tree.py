from __future__ import annotations

from typing import TYPE_CHECKING, List

from discoursesimplification.utils import pretty_tree_printer

if TYPE_CHECKING:
    from discoursesimplification.runner.discourse_tree.model.leaf import Leaf


# This class should normally be abstract
class DiscourseTree:

    def __init__(self, extraction_rule: str):
        self.extraction_rule = extraction_rule
        self.processed = False
        self.parent = None  # should be set by inherited classes
        self.sentence_index = -1  # should be set by inherited classes

    def set_recursive_unset_sentence_index(self, sentence_index: int):
        if self.sentence_index < 0:
            self.sentence_index = sentence_index
            # the rest (recursive) implemented in subclasses (Coordination and Subordination)

    def clean_up(self):
        pass  # implemented in subclasses (Coordination and Subordination)

    def usable_as_reference(self):
        pass  # implemented in subclasses

    def use_as_reference(self):
        if self.usable_as_reference():
            self.parent.invalidate_coordination(self)
        else:
            raise AssertionError("Not useable as reference")

    def get_core_path_leaves(self) -> List[Leaf]:
        return []  # implemented in subclasses

    def parent_get_previous_node(self) -> DiscourseTree:
        pass  # implemented in subclasses

    def get_previous_node(self) -> DiscourseTree:
        if self.parent is not None:
            p = self.parent

            res = p.parent_get_previous_node()
            if res is not None:
                return res
            # recursion
            return self.parent.get_previous_node()

        return None

    def is_not_processed(self) -> bool:
        return not self.processed

    def __str__(self):
        return pretty_tree_printer.pretty_print(self, False)
