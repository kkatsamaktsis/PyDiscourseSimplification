from typing import List

from nltk.tree import Tree


class NodeInstance:
    def __init__(self, node, instance_number: int):
        self.node = node
        self.instance_number = instance_number

    def __str__(self):
        return "[" + str(self.node) + ", Instance number: " + str(self.instance_number) + "]"


class MutableInteger:
    def __init__(self, value):
        self.int_value = value

    def inc_value(self, value):
        self.int_value += value

    def __str__(self):
        return str(self.int_value)


# The tree is assumed to have Word objects as leaves.
def get_value(node: Tree):
    return node.label().value if isinstance(node, list) else node.value


def first_child(node: Tree):
    if not isinstance(node, list):
        return None
    return node[0]


# Returns the node labeled with {@code name} in the pattern.
def matcher_get_node(match, name: str) -> Tree:
    for i in range(0, len(match['namedNodes'])):
        if name in match['namedNodes'][i]:
            node = Tree.fromstring(match['namedNodes'][i][name]['match'])
            return node
    return None


# Returns the first subtree from the give parse_tree equal to the match
# labeled with {@code name} in the pattern.
def matcher_get_node_from_tree(parse_tree: Tree, match, name: str) -> Tree:
    for i in range(0, len(match['namedNodes'])):
        if name in match['namedNodes'][i]:
            node_str = match['namedNodes'][i][name]['match']

            for subtree in parse_tree.subtrees(lambda t: t == Tree.fromstring(node_str)):
                return subtree
    return None


# Gets the leaves of the tree.
def get_leaves(tree: Tree, tree_list: List[Tree]):
    if not isinstance(tree, list):
        tree_list.append(tree)
    else:
        if isinstance(tree, list):
            for child in tree:
                get_leaves(child, tree_list)
    return tree_list


def add_node_numbers_to_tree(root: Tree, curr_node_number: int):
    setattr(root, "node_number", curr_node_number)
    if isinstance(root, list):
        for child in root:
            curr_node_number += 1
            add_node_numbers_to_tree(child, curr_node_number)


def node_number_helper(node: Tree, t: Tree, i: MutableInteger):
    if node == t:
        return True
    i.inc_value(1)
    if isinstance(t, list):
        for j in range(0, len(t)):
            if node_number_helper(node, t[j], i):
                return True
    return False


# This method is deprecated. It returns the number of the given node in a depth-first search
# traversal but nodes are compared by *value* *not reference*. This means that if at least two
# nodes exists in the tree with the same structure and values, e.e. (, ,), then always the first 
# one will be returned.
def node_number(node: Tree, root: Tree) -> any:
    i = MutableInteger(1)
    if node_number_helper(node, root, i):
        return i.int_value
    return -1


def node_number_helper_instance_based(node: Tree, t: Tree, i: MutableInteger):
    if node is t:
        return True
    i.inc_value(1)
    if isinstance(t, list):
        for j in range(0, len(t)):
            if node_number_helper_instance_based(node, t[j], i):
                return True
    return False


def node_number_instance_based(node: Tree, root: Tree) -> any:
    i = MutableInteger(1)
    if node_number_helper_instance_based(node, root, i):
        return i.int_value
    return -1


def node_number_helper_instance_number_based(node: Tree, instance: int, t, i: MutableInteger,
                                             curr_inst: MutableInteger):
    if node == t:
        if instance == curr_inst.int_value:
            return True
        else:
            curr_inst.inc_value(1)
    i.inc_value(1)
    if isinstance(t, list):
        for j in range(0, len(t)):
            if node_number_helper_instance_number_based(node, instance, t[j], i, curr_inst):
                return True
    return False


def node_number_instance_number_based(node: Tree, instance: int, root: Tree) -> any:
    i = MutableInteger(1)
    curr_inst = MutableInteger(1)
    if node_number_helper_instance_number_based(node, instance, root, i, curr_inst):
        return i.int_value
    return -1


def get_node_number_helper(node: Tree, i: MutableInteger, target: int):
    i1 = i.int_value
    if i1 == target:
        return node
    if i1 > target:
        raise IndexError("Error -- tree does not contain " + str(i) + " nodes.")
    i.inc_value(1)
    if isinstance(node, list):
        for j in range(0, len(node)):
            temp = get_node_number_helper(node[j], i, target)
            if temp is not None:
                return temp
    return None


def get_node_number(node: Tree, i: int) -> any:
    return get_node_number_helper(node, MutableInteger(1), i)


def parent_helper(parent_tree: Tree, kids: List[any], node: Tree):
    for kid in kids:
        if kid == node:
            return parent_tree
        ret = parent_helper(kid, kid, node)
        if ret is not None:
            return ret
    return None


# TODO replace this with parent_instance_based?
def parent(node: Tree, root: Tree):
    kids = node if isinstance(node, list) else []
    return parent_helper(root, kids, node)


def get_children_helper(node: Tree):
    return node if isinstance(node, list) else []


def parent_helper_instance_based(parent_tree: Tree, kids: List[any], node: Tree):
    for kid in kids:
        if kid is node:
            return parent_tree
        ret = parent_helper_instance_based(kid, get_children_helper(kid), node)
        if ret is not None:
            return ret
    return None


def parent_instance_based(node: Tree, root: Tree):
    kids = get_children_helper(root)
    return parent_helper_instance_based(root, kids, node)
