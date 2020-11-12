from __future__ import annotations
from typing import List, TYPE_CHECKING
from discoursesimplification.utils import tree_utils

if TYPE_CHECKING:
    pass

from nltk.tree import Tree


class INodeChecker:
    def check(self, anchor_tree, node) -> bool:
        return False  # Implemented in subclasses


def get_leaf_numbers(anchor_tree, node):
    res = []
    for leaf in tree_utils.get_leaves(node, []):
        res.append(tree_utils.node_number_instance_based(leaf, anchor_tree))
    return res


def yield_words(tree: Tree, y: list):
    if not isinstance(tree, list):
        y.append(tree_utils.get_value(tree))
    else:
        for kid in tree:
            yield_words(kid, y)
    return y


def leaves_to_words(leaves: List[any]):
    return list(map(lambda l: yield_words(l, [])[0], leaves))


def split_leaves(anchor_tree: Tree, leaves: List[Tree], leaf_checker: INodeChecker, remove_empty: bool) -> List[List[Tree]]:
    res = []
    curr_element = []
    for leaf in leaves:
        if leaf_checker.check(anchor_tree, leaf):
            if len(curr_element) > 0 or not remove_empty:
                res.append(curr_element)
            curr_element = []
        else:
            curr_element.append(leaf)

    if len(curr_element) > 0 or not remove_empty:
        res.append(curr_element)

    return res


def find_leaves(anchor_tree: Tree, leaves: List[Tree], leaf_checker: INodeChecker, to_reverse: bool) -> List[Tree]:
    res = list(filter(lambda l: leaf_checker.check(anchor_tree, l), leaves))
    if to_reverse:
        res.reverse()
    return res


def get_first_leaf(tree: Tree):
    if not isinstance(tree, list):
        return tree
    else:
        return get_first_leaf(tree[0])


def get_last_leaf(tree: Tree):
    if not isinstance(tree, list):
        return tree
    else:
        return get_last_leaf(tree[len(tree) - 1])


def get_leaves_in_between(anchor_tree: Tree, left_node: Tree, right_node: Tree, include_left: bool, include_right: bool):
    res = []

    if left_node is None:
        left_node = get_first_leaf(anchor_tree)

    if right_node is None:
        right_node = get_last_leaf(anchor_tree)

    if include_left:
        start_leaf_number = tree_utils.node_number_instance_based(get_first_leaf(left_node), anchor_tree)
    else:
        start_leaf_number = tree_utils.node_number_instance_based(get_last_leaf(left_node), anchor_tree) + 1

    if include_right:
        end_leaf_number = tree_utils.node_number_instance_based(get_last_leaf(right_node), anchor_tree)
    else:
        end_leaf_number = tree_utils.node_number_instance_based(get_first_leaf(right_node), anchor_tree) - 1

    if start_leaf_number < 0 or end_leaf_number < 0:
        return res

    for i in range(start_leaf_number, end_leaf_number + 1):
        node = tree_utils.get_node_number(anchor_tree, i)
        if not isinstance(node, list):
            res.append(node)

    return res


def get_preceding_leaves(anchor_tree, node, include: bool):
    return get_leaves_in_between(anchor_tree, get_first_leaf(anchor_tree), node, True, include)


def get_following_leaves(anchor_tree, node, include: bool):
    return get_leaves_in_between(anchor_tree, node, get_last_leaf(anchor_tree), include, True)


def get_containing_leaves(node):
    return get_leaves_in_between(node, get_first_leaf(node), get_last_leaf(node), True, True)


def get_words_in_between(anchor_tree, left_node, right_node, include_left: bool, include_right: bool):
    return leaves_to_words(get_leaves_in_between(anchor_tree, left_node, right_node, include_left, include_right))


def get_preceding_words(anchor_tree, node, include: bool):
    return leaves_to_words(get_preceding_leaves(anchor_tree, node, include))


def get_following_words(anchor_tree, node, include: bool):
    return leaves_to_words(get_following_leaves(anchor_tree, node, include))


def get_containing_words(node):
    return leaves_to_words(get_containing_leaves(node))


def get_leaves_in_between_numbered_node_instances(anchor_tree, left_node, left_instance_number: int,
                                                  right_node, right_instance_number: int,
                                                  include_left: bool, include_right: bool):
    res = []

    if left_node is None:
        left_node = get_first_leaf(anchor_tree)

    if right_node is None:
        right_node = get_last_leaf(anchor_tree)

    if include_left:
        start_leaf_number = tree_utils \
            .node_number_instance_number_based(get_first_leaf(left_node), left_instance_number, anchor_tree)
    else:
        start_leaf_number = tree_utils \
                                .node_number_instance_number_based(get_last_leaf(left_node), left_instance_number, anchor_tree) + 1

    if include_right:
        end_leaf_number = tree_utils \
            .node_number_instance_number_based(get_last_leaf(right_node), right_instance_number, anchor_tree)
    else:
        end_leaf_number = tree_utils \
                              .node_number_instance_number_based(get_first_leaf(right_node), right_instance_number, anchor_tree) - 1

    if start_leaf_number < 0 or end_leaf_number < 0:
        return res

    for i in range(start_leaf_number, end_leaf_number + 1):
        node = tree_utils.get_node_number(anchor_tree, i)
        if not isinstance(node, list):
            res.append(node)

    return res


def get_following_leaves_numbered_node_instance(anchor_tree, node, instance_number: int, include: bool):
    return get_leaves_in_between_numbered_node_instances(anchor_tree, node, instance_number,
                                                         get_last_leaf(anchor_tree), 1, include, True)


# The alternative method get_following_words would return the words following the first instance of
# a node equal to node, while this method returns the words following the given node after its instance_number-th time.
def get_following_words_numbered_node_instance(anchor_tree, node, instance_number: int, include: bool):
    return leaves_to_words(get_following_leaves_numbered_node_instance(anchor_tree, node, instance_number, include))


def find_spanning_tree_rec(anchor_tree: Tree, curr_tree: Tree, first_leaf: Tree, last_leaf: Tree) -> Tree:
    first_number = tree_utils.node_number_instance_based(first_leaf, anchor_tree)
    last_number = tree_utils.node_number_instance_based(last_leaf, anchor_tree)
    curr_first_number = tree_utils.node_number_instance_based(get_first_leaf(curr_tree), anchor_tree)
    curr_last_number = tree_utils.node_number_instance_based(get_last_leaf(curr_tree), anchor_tree)
    if curr_first_number <= first_number <= curr_last_number and curr_first_number <= last_number <= curr_last_number:
        if curr_first_number == first_number and last_number == curr_last_number:
            return curr_tree
        else:
            # recursion
            for child in curr_tree:
                cr = find_spanning_tree_rec(anchor_tree, child, first_leaf, last_leaf)
                if cr is not None:
                    return cr
    return None


def find_spanning_tree(anchor_tree: Tree, first_leaf: Tree, last_leaf: Tree) -> Tree:
    return find_spanning_tree_rec(anchor_tree, anchor_tree, first_leaf, last_leaf)

