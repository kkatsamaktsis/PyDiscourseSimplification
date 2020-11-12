from typing import List


class DefaultEdge:
    def __init__(self, caption: str, child, follow_ptp_child: bool):
        self.caption = caption
        self.child = child
        self.follow_ptp_child = follow_ptp_child
        

def trim_text(text: str, max_text_len: int) -> str:
    suffix = "..."

    if max_text_len is not None and len(text) > max_text_len:
        if max_text_len < len(suffix):
            raise ValueError("maxTextLen should have at least the length: " + str(len(suffix)))

        return text[0:(max_text_len - len(suffix))] + suffix
    else:
        return text


def get_bottom_depth(node, follow: bool) -> int:
    if not follow or len(node.get_ptp_edges()) <= 0:
        return 0
    else:
        return max(
            list(map(lambda e: get_bottom_depth(e.child, e.follow_ptp_child), node.get_ptp_edges()))) + 1


def get_edge_indent(size: int, edge_caption: str, last_child: bool) -> str:
    front = "└─" if last_child else "├─"
    back = "─> "

    middle = trim_text(edge_caption, size - len(front) - len(back))

    right = True
    while len(front) + len(middle) + len(back) < size:
        middle = middle + "─" if right else "─" + middle
        right = not right

    return front + middle + back


def get_indent(size: int, last_child: bool) -> str:
    res = " " if last_child else "|"
    while len(res) < size:
        res = res + " "

    return res


def pretty_print_rec(node, follow: bool, reverse: bool, size: int) -> List[str]:
    res = []

    bottom_depth = get_bottom_depth(node, follow)

    # this node
    res.extend(node.get_ptp_caption())

    # edges
    if follow:
        edges = node.get_ptp_edges()
        if reverse:
            edges = list(reversed(node.get_ptp_edges()))

        for i in range(0, len(edges)):
            edge = edges[i]
            end_child = i == len(edges) - 1
            indent_size = (bottom_depth - get_bottom_depth(edge.child, edge.follow_ptp_child)) * size

            first_child_line = True
            for child_line in pretty_print_rec(edge.child, edge.follow_ptp_child, reverse, size):
                if first_child_line:
                    res.append(get_edge_indent(indent_size, edge.caption, end_child) + child_line)
                    first_child_line = False
                else:
                    res.append(get_indent(indent_size, end_child) + child_line)
    return res


def pretty_print(node, reverse: bool = False, size: int = 10) -> str:
    return "\n".join(pretty_print_rec(node, True, reverse, size))
