from discoursesimplification.runner.discourse_tree.extraction.extraction import Extraction
from discoursesimplification.runner.discourse_tree.extraction.extraction_rule import ExtractionRule
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.words import words_utils
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf
from discoursesimplification.utils import tree_utils

from discoursesimplification import config


class SharedNPPostParticipalExtractor(ExtractionRule):
    def __init__(self):
        super().__init__()

    def extract(self, leaf: Leaf) -> Extraction:
        participal_node = "(__=node [== S=s | == (PP|ADVP <+(PP|ADVP) S=s)]) : (=s <: (VP <<, VBG|VBN=vbgn))"
        p = "ROOT <<: (S < (NP=np $.. (VP=vp <+(VP) (NP|PP $.. " + participal_node + "))))"
        matches = config.corenlp_client.tregex(leaf.text, p)

        if len(matches['sentences'][0]) > 0:
            match = matches['sentences'][0][str(0)]
            matched_node_s = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "s")
            matched_node_node = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "node")
            matched_node_np = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "np")
            matched_node_vp = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "vp")
            matched_node_vbgn = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "vbgn")

            cue_phrase_words = parse_tree_extraction_utils.get_preceding_words(matched_node_node, matched_node_s, False)

            # the left, superordinate constituent
            left_constituent_words = []

            # the left, superordinate constituent
            left_constituent_words.extend(
                parse_tree_extraction_utils.get_preceding_words(leaf.parse_tree, matched_node_s, False))
            left_constituent_words.extend(
                parse_tree_extraction_utils.get_following_words(leaf.parse_tree, matched_node_s, False))
            left_constituent = Leaf(self.__class__.__name__, None,
                                    words_utils.words_to_proper_sentence_string(left_constituent_words))

            # the right, subordinate constituent
            right_constituent_words = []
            right_constituent_words.extend(parse_tree_extraction_utils.get_preceding_words(
                leaf.parse_tree, matched_node_vp, False))
            right_constituent_words.extend(self.get_rephrased_participal_s(
                matched_node_np, matched_node_vp, matched_node_s, matched_node_vbgn))
            right_constituent_words.extend(parse_tree_extraction_utils.get_following_words(
                leaf.parse_tree, matched_node_s, False))
            right_constituent = Leaf(self.__class__.__name__, None,
                                     words_utils.words_to_proper_sentence_string(right_constituent_words))

            # relation
            relation = self.classifier.classify_subordinating(cue_phrase_words)
            if relation is None:
                relation = Relation.UNKNOWN_COORDINATION

            res = Extraction(self.__class__.__name__, False, None, relation,
                             True, [left_constituent, right_constituent])

            return res

        return None
