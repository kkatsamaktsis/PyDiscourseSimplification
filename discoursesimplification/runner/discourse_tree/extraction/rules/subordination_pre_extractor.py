from discoursesimplification.runner.discourse_tree.extraction.extraction import Extraction
from discoursesimplification.runner.discourse_tree.extraction.extraction_rule import ExtractionRule
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.words import words_utils
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf
from discoursesimplification.utils import tree_utils

from discoursesimplification import config


class SubordinationPreExtractor(ExtractionRule):
    def __init__(self):
        super().__init__()

    def extract(self, leaf: Leaf) -> Extraction:
        p = "ROOT <<: (S < (SBAR=sbar < (S=s < (NP $.. VP)) $.. (NP $.. VP)))"
        matches = config.corenlp_client.tregex(leaf.text, p)

        if len(matches['sentences'][0]) > 0:
            match = matches['sentences'][0][str(0)]
            matched_node_sbar = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "sbar")
            matched_node_s = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "s")

            # the left, subordinate constituent
            left_constituent_words = parse_tree_extraction_utils.get_containing_words(matched_node_s)
            left_constituent = Leaf(self.__class__.__name__, None,
                                    words_utils.words_to_proper_sentence_string(left_constituent_words))

            # the right, superordinate constituent
            right_constituent_words = []
            right_constituent_words.extend(parse_tree_extraction_utils.get_preceding_words(
                leaf.parse_tree, matched_node_sbar, False))

            right_constituent_words.extend(parse_tree_extraction_utils.get_following_words(
                leaf.parse_tree, matched_node_sbar, False))

            right_constituent = Leaf(self.__class__.__name__, None,
                                     words_utils.words_to_proper_sentence_string(right_constituent_words))

            # relation
            cue_phrase_words = parse_tree_extraction_utils.get_preceding_words(
                tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "sbar"),
                tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "s"), False)
            relation = self.classifier.classify_subordinating(cue_phrase_words)
            if relation is None:
                relation = Relation.UNKNOWN_SUBORDINATION

            res = Extraction(self.__class__.__name__, False, cue_phrase_words, relation, False,
                             [left_constituent, right_constituent])

            return res
        return None
