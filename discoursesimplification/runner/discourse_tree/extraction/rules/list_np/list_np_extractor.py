from discoursesimplification.runner.discourse_tree.extraction.extraction import Extraction
from discoursesimplification.runner.discourse_tree.extraction.extraction_rule import ExtractionRule
from discoursesimplification.runner.discourse_tree.extraction.utils.list_np_splitter import ListNPSplitter
from discoursesimplification.utils import tree_utils
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.words import words_utils
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf

from discoursesimplification import config


class ListNPExtractor(ExtractionRule):
    def __init__(self, pattern: str):
        super().__init__()
        self.pattern = pattern

    def extract(self, leaf: Leaf) -> Extraction:
        p = self.pattern
        matches = config.corenlp_client.tregex(leaf.text, p)

        if len(matches['sentences'][0]) > 0:  # range(0, len(matches['sentences'][0])):
            match = matches['sentences'][0][str(0)]
            matched_node_np = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "np")

            r = ListNPSplitter.split_list(leaf.parse_tree, matched_node_np)
            if r is not None:

                # constituents
                preceding_words = parse_tree_extraction_utils.get_preceding_words(
                    leaf.parse_tree, matched_node_np, False)
                following_words = parse_tree_extraction_utils.get_following_words(
                    leaf.parse_tree, matched_node_np, False)

                constituents = []

                if r.introduction_words is not None:
                    words = []
                    words.extend(preceding_words)
                    words.extend(r.introduction_words)
                    words.extend(following_words)

                    constituent = Leaf(self.__class__.__name__, None,
                                       words_utils.words_to_proper_sentence_string(words))
                    constituent.allow_split = False
                    constituents.append(constituent)

                for element in r.elements_words:
                    words = []
                    words.extend(preceding_words)
                    words.extend(element)
                    words.extend(following_words)

                    constituent = Leaf(self.__class__.__name__, None,
                                       words_utils.words_to_proper_sentence_string(words))
                    constituent.allow_split = False
                    constituents.append(constituent)

                res = Extraction(self.__class__.__name__, False, None, r.relation, True, constituents)

                return res

        return None

