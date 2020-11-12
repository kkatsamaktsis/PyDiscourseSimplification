from typing import List

from discoursesimplification.runner.discourse_tree.model.discourse_tree import DiscourseTree
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.runner.discourse_tree.model.invalidation import Invalidation
from discoursesimplification.utils.pretty_tree_printer import DefaultEdge


class Coordination(DiscourseTree):

    def __init__(self, extraction_rule: str, relation: Relation, cue_phrase: str, coordinations: List[DiscourseTree]):
        super().__init__(extraction_rule)
        self.relation = relation
        self.cue_phrase = cue_phrase
        self.coordinations = []
        for coordination in coordinations:
            self.add_coordination(coordination)
        self.is_coordination = True

    def set_recursive_unset_sentence_index(self, sentence_index: int):
        if self.sentence_index < 0:
            self.sentence_index = sentence_index
            # recursive
            for coordination in self.coordinations:
                coordination.set_recursive_unset_sentence_index(sentence_index)

    def clean_up(self):
        # remove invalidations
        self.remove_invalidations()
        #  recursion
        for coordination in self.coordinations:
            coordination.clean_up()

    def usable_as_reference(self):
        return (self.parent is not None) \
               and isinstance(self.parent, Coordination) and self.parent.relation == Relation.UNKNOWN

    def get_core_path_leaves(self) -> List[Leaf]:
        res = []

        # recursion on coordinations
        for child in self.coordinations:
            res.extend(child.get_core_path_leaves())

        return res

    def parent_get_previous_node(self) -> DiscourseTree:
        prev = None
        for child in self.coordinations:
            if child == self and prev is not None:
                return prev
            prev = child
        return None

    def add_coordination(self, coordination: DiscourseTree):
        self.coordinations.append(coordination)
        coordination.parent = self

    def invalidate_coordination(self, coordination: DiscourseTree):
        self.replace_coordination(coordination, Invalidation())

    def replace_coordination(self, old_coordination: DiscourseTree, new_coordination: DiscourseTree):
        for i in range(0, len(self.coordinations)):
            if self.coordinations[i] == old_coordination:
                self.coordinations[i] = new_coordination
                new_coordination.parent = self
                new_coordination.set_recursive_unset_sentence_index(old_coordination.sentence_index)
                break

    def remove_invalidations(self):
        for i in range(len(self.coordinations) - 1, -1, -1):
            if isinstance(self.coordinations[i], Invalidation):
                del self.coordinations[i]

    def get_other_preceding_coordinations(self, coordination: DiscourseTree):
        res = []
        for child in self.coordinations:
            if child == coordination:
                break
            else:
                res.append(child)
        return res

    def get_other_following_coordinations(self, coordination: DiscourseTree):
        res = []

        found = False
        for child in self.coordinations:
            if child == coordination:
                found = True
            else:
                if found:
                    res.append(child)
        return res

    # VISUALIZATION
    def get_ptp_caption(self) -> List[str]:
        cue_phrase_str = "'" + self.cue_phrase + "'" if self.cue_phrase is not None else "NULL"
        return ["CO/" + str(self.relation.value) + " (" + cue_phrase_str + ", " + self.extraction_rule + ")"]

    def get_ptp_edges(self) -> List[DefaultEdge]:
        return list(map(lambda c: DefaultEdge("n", c, True), self.coordinations))
