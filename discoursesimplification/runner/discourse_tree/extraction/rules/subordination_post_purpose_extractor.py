from discoursesimplification.runner.discourse_tree.extraction.extraction import Extraction
from discoursesimplification.runner.discourse_tree.extraction.extraction_rule import ExtractionRule
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.utils import tree_utils
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.words import words_utils
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf

from discoursesimplification import config


class SubordinationPostPurposeExtractor(ExtractionRule):
    def __init__(self):
        super().__init__()

    def extract(self, leaf: Leaf) -> Extraction:
        p = "ROOT <<: (S < (NP $.. (VP=vp <+(VP) (SBAR=sbar < (S=s <<, (VP <<, /(T|t)o/))))))"
        matches = config.corenlp_client.tregex(leaf.text, p)

        if len(matches['sentences'][0]) > 0:  # range(0, len(matches['sentences'][0])):
            match = matches['sentences'][0][str(0)]
            matched_node_sbar = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "sbar")
            matched_node_s = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "s")
            matched_node_vp = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "vp")

            # the left, superordinate constituent
            left_constituent_words = []
            left_constituent_words.extend(parse_tree_extraction_utils.get_preceding_words(
                leaf.parse_tree, matched_node_sbar, False))
            left_constituent_words.extend(parse_tree_extraction_utils.get_following_words(
                leaf.parse_tree, matched_node_sbar, False))
            left_constituent = Leaf(self.__class__.__name__, None,
                                    words_utils.words_to_proper_sentence_string(left_constituent_words))

            # rephrase
            right_constituent_words = self.rephrase_enablement(matched_node_s, matched_node_vp)
            right_constituent = Leaf(self.__class__.__name__, None,
                                     words_utils.words_to_proper_sentence_string(right_constituent_words))
            right_constituent.allow_split = False
            right_constituent.to_simple_context = True

            # relation
            relation = Relation.PURPOSE

            res = Extraction(self.__class__.__name__, False, None, relation,
                             True, [left_constituent, right_constituent])

            return res

        return None

