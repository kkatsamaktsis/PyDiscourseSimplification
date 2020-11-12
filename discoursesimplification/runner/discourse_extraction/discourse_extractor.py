from __future__ import annotations

from typing import List

from discoursesimplification.model.element import Element
from discoursesimplification.model.linked_context import LinkedContext
from discoursesimplification.model.simple_context import SimpleContext
from discoursesimplification.runner.discourse_tree import relation_utility
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.runner.discourse_tree.model.discourse_tree import DiscourseTree
from discoursesimplification.runner.discourse_tree.model.coordination import Coordination
from discoursesimplification.runner.discourse_tree.model.subordination import Subordination
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf
from discoursesimplification.config import Config


class DiscourseExtractor:

    def __init__(self):
        self.ignored_relations = []
        for ignored_relation in Config.ignored_relations:
            self.ignored_relations.append(relation_utility.str_to_relation(ignored_relation))

        self.processed_leaves = {}

    def do_discourse_extraction(self, discourse_tree: DiscourseTree) -> List[Element]:
        self.processed_leaves = {}
        self.__extract_rec(discourse_tree, 0)
        return list(self.processed_leaves.values())

    def __add_as_context(self, leaf: Leaf, target_leaf: Leaf, target_relation: Relation) -> None:
        if leaf.to_simple_context:
            return
        leaf_element = self.processed_leaves[leaf]

        if target_leaf.to_simple_context:
            # simple context
            sc = SimpleContext(target_leaf.parse_tree)
            sc.set_relation(target_relation)
            leaf_element.add_simple_context(sc)
        else:
            # linked context
            target_element = self.processed_leaves[target_leaf]
            leaf_element.add_linked_context(LinkedContext(target_element.id, target_relation))

    def __extract_rec(self, node: DiscourseTree, context_layer: int) -> None:
        if isinstance(node, Leaf):
            leaf = node
            if not leaf.to_simple_context:

                # create new element
                element = Element(leaf.parse_tree, leaf.sentence_index, context_layer)

                self.processed_leaves[leaf] = element

        if isinstance(node, Coordination):
            coordination = node

            # recursion
            for child in coordination.coordinations:
                self.__extract_rec(child, context_layer)

            # set relations
            if coordination.relation not in self.ignored_relations:
                for child in coordination.coordinations:
                    child_n_leaves = child.get_core_path_leaves()

                    # forward direction
                    for sibling in coordination.get_other_following_coordinations(child):
                        sibling_n_leaves = sibling.get_core_path_leaves()

                        for child_n_leaf in child_n_leaves:
                            for sibling_n_leaf in sibling_n_leaves:
                                self.__add_as_context(child_n_leaf, sibling_n_leaf, coordination.relation)

                    # inverse direction
                    for sibling in coordination.get_other_preceding_coordinations(child):
                        sibling_n_leaves = sibling.get_core_path_leaves()

                        for child_n_leaf in child_n_leaves:
                            for sibling_n_leaf in sibling_n_leaves:
                                self.__add_as_context(child_n_leaf, sibling_n_leaf,
                                                      relation_utility.get_inverse(coordination.relation))

        if isinstance(node, Subordination):
            subordination = node

            # recursion
            self.__extract_rec(subordination.get_superordination(), context_layer)
            self.__extract_rec(subordination.get_subordination(), context_layer + 1)

            # add relations
            if subordination.relation not in self.ignored_relations:
                superordination_n_leaves = subordination.get_superordination().get_core_path_leaves()
                subordination_n_leaves = subordination.get_subordination().get_core_path_leaves()

                for superordination_n_leaf in superordination_n_leaves:
                    for subordination_n_leaf in subordination_n_leaves:
                        self.__add_as_context(superordination_n_leaf, subordination_n_leaf, subordination.relation)
