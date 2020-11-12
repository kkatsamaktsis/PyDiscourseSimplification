from typing import List

from discoursesimplification.utils import tree_utils, pretty_tree_printer
from discoursesimplification.utils.pretty_tree_printer import DefaultEdge

from nltk.tree import Tree


class MyTreeNode(object):
    def __init__(self, parse_node: Tree, anchor: Tree):
        self.caption = tree_utils.get_value(parse_node)
        self.children = []
        if isinstance(parse_node, list):
            for child_node in parse_node:
                self.children.append(MyTreeNode(child_node, anchor))
        
        self.nr = tree_utils.node_number_instance_based(parse_node, anchor)

    def get_ptp_caption(self) -> List[str]:
        return [self.caption, "#" + str(self.nr)]

    def get_ptp_edges(self):
        return list(map(lambda c: DefaultEdge("", c, True), self.children))


def pretty_print(parse_tree: Tree):
    node = MyTreeNode(parse_tree, parse_tree)
    return pretty_tree_printer.pretty_print(node, False)
