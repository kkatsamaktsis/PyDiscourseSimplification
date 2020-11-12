from __future__ import annotations
from typing import TYPE_CHECKING

from discoursesimplification.runner.discourse_tree.relation import Relation

if TYPE_CHECKING:
    from discoursesimplification.model.simplification_content import SimplificationContent


class LinkedContext:

    def __init__(self, target_id: str, relation: Relation):
        self.target_id = target_id
        self.relation = relation

    def get_target_element(self, content: SimplificationContent):
        return content.get_element(self.target_id)

    def __eq__(self, other):
        return (isinstance(other, LinkedContext)
                and other.target_id == self.target_id and other.relation == self.relation)
