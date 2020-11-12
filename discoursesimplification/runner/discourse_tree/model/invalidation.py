from __future__ import annotations

from typing import List

from discoursesimplification.runner.discourse_tree.model.discourse_tree import DiscourseTree
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.utils.pretty_tree_printer import DefaultEdge


class Invalidation(DiscourseTree):

    def __init__(self):
        super().__init__("")

    def get_previous_node(self) -> DiscourseTree:
        pass

    def usable_as_reference(self):
        return (self.parent is not None) \
               and self.parent.is_coordination and self.parent.relation == Relation.UNKNOWN

    # VISUALIZATION
    def get_ptp_caption(self) -> List[str]:
        return ["INVALIDATED"]

    def get_ptp_edges(self) -> List[DefaultEdge]:
        return []
