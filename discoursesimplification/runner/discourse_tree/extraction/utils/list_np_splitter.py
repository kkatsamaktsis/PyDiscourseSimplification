from typing import List

from nltk import Tree

from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.utils import tree_utils
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils


class Result:
    def __init__(self, introduction_words: List[str], elements_words: List[str], relation: Relation):
        self.introduction_words = introduction_words  # optional
        self.elements_words = elements_words
        self.relation = relation


class ConjunctionLeafChecker(parse_tree_extraction_utils.INodeChecker):
    def __init__(self, word: str):
        self.word = word

    def check(self, anchor_tree: Tree, leaf: Tree) -> bool:
        return parse_tree_extraction_utils.yield_words(leaf, [])[0] == self.word \
               and tree_utils.parent_instance_based(leaf, anchor_tree) is not None \
               and tree_utils.get_value(tree_utils.parent_instance_based(leaf, anchor_tree)) == "CC"


class ValueLeafChecker(parse_tree_extraction_utils.INodeChecker):
    def __init__(self, word: str):
        self.word = word

    def check(self, anchor_tree: Tree, leaf: Tree) -> bool:
        return tree_utils.get_value(leaf) == self.word


class ListNPSplitter:

    @staticmethod
    def check_element_leaves(anchor_tree: Tree, leaves: List[Tree]) -> bool:
        spanning_tree = parse_tree_extraction_utils.find_spanning_tree(anchor_tree, leaves[0], leaves[len(leaves) - 1])
        return spanning_tree is not None and tree_utils.get_value(spanning_tree) == "NP"

    @staticmethod
    def is_followed_by_conj_disjunction(anchor_tree: Tree, np: Tree,
                                        conj_disj_checker: parse_tree_extraction_utils.INodeChecker,
                                        separator_checker: parse_tree_extraction_utils.INodeChecker) -> bool:
        following_leaves = parse_tree_extraction_utils.get_following_leaves(anchor_tree, np, False)
        
        for following_leaf in following_leaves:
            if conj_disj_checker.check(anchor_tree, following_leaf):
                return True
            elif separator_checker.check(anchor_tree, following_leaf):
                pass  # nothing
            else:
                return False
        return False

    @staticmethod
    def check(anchor_tree: Tree, np: Tree, conj_disj_checker: parse_tree_extraction_utils.INodeChecker,
              separator_checker: parse_tree_extraction_utils.INodeChecker, relation: Relation) -> Result:
        check_leaves = parse_tree_extraction_utils.get_containing_leaves(np)

        # find introduction
        introduction_words = None
        intro_separators = parse_tree_extraction_utils.find_leaves(anchor_tree, check_leaves, ValueLeafChecker(":"),
                                                                   False)
        if len(intro_separators) > 0:
            iws = parse_tree_extraction_utils.get_preceding_words(np, intro_separators[0], False)
            if len(iws) > 0:
                introduction_words = iws
                check_leaves = parse_tree_extraction_utils.get_following_leaves(np, intro_separators[0], False)

        if len(check_leaves) == 0:
            return None

        # special case (Con/Disjunction is right after the NP e.g. initiating a verb phrase)
        # e.g. "To leave monuments to his reign , he built
        # [the Collège des Quatre-Nations , Place Vendôme , Place des Victoires ,] and began Les Invalides ."
        if ListNPSplitter.is_followed_by_conj_disjunction(anchor_tree, np, conj_disj_checker, separator_checker):
            elements = parse_tree_extraction_utils.split_leaves(np, check_leaves, separator_checker, True)
            valid = True

            # check elements
            if len(elements) >= 2:
                for element in elements:
                    if not(ListNPSplitter.check_element_leaves(np, element)):
                        valid = False
                        break
            else:
                valid = False

            if valid:
                elements_words = list(map(lambda e: parse_tree_extraction_utils.leaves_to_words(e), elements))

                return Result(introduction_words, elements_words, relation)

        # check different conjunction/disjunction leaves (from right to left)
        for cd_leaf in parse_tree_extraction_utils.find_leaves(np, check_leaves, conj_disj_checker, True):
            valid = True
            before_leaves = parse_tree_extraction_utils.get_leaves_in_between(
                np, check_leaves[0], cd_leaf, True, False)
            after_leaves = parse_tree_extraction_utils.get_leaves_in_between(
                np, cd_leaf, check_leaves[len(check_leaves) - 1], False, True)

            before_elements = parse_tree_extraction_utils.split_leaves(np, before_leaves, separator_checker, True)
            after_element = after_leaves

            # check before elements
            if len(before_elements) >= 1:
                for before_element in before_elements:
                    if not(ListNPSplitter.check_element_leaves(np, before_element)):
                        valid = False
                        break
            else:
                valid = False

            # check after element
            if len(after_element) >= 1:
                pass
            else:
                valid = False

            if valid:
                elements_words = []
                elements_words.extend(list(map(lambda e: parse_tree_extraction_utils.leaves_to_words(e),
                                               before_elements)))
                elements_words.append(parse_tree_extraction_utils.leaves_to_words(after_leaves))

                return Result(introduction_words, elements_words, relation)

        return None

    @staticmethod
    def split_list(anchor_tree: Tree, np: Tree) -> Result:
        contains_semicolon = len(parse_tree_extraction_utils.find_leaves(
            np, parse_tree_extraction_utils.get_containing_leaves(np), ValueLeafChecker(";"), False)) > 0

        if contains_semicolon:

            # check for conjunction with elements separated by ;
            r = ListNPSplitter.check(anchor_tree, np, ConjunctionLeafChecker("and"),
                                     ValueLeafChecker(";"), Relation.LIST)
            if r is not None:
                return r

            # check for disjunction with elements separated by ;
            r = ListNPSplitter.check(anchor_tree, np, ConjunctionLeafChecker("or"),
                                     ValueLeafChecker(";"), Relation.DISJUNCTION)
            if r is not None:
                return r
        else:

            # check for conjunction with elements separated by ,
            r = ListNPSplitter.check(anchor_tree, np, ConjunctionLeafChecker("and"),
                                     ValueLeafChecker(","), Relation.LIST)

            if r is not None:
                return r

            # check for disjunction with elements separated by ,
            r = ListNPSplitter.check(anchor_tree, np, ConjunctionLeafChecker("or"),
                                     ValueLeafChecker(","), Relation.DISJUNCTION)
            if r is not None:
                return r

        return None
