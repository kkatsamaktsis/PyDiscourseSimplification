from discoursesimplification.runner.discourse_tree.extraction.extraction import Extraction
from discoursesimplification.runner.discourse_tree.extraction.extraction_rule import ExtractionRule
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.words import words_utils
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf
from discoursesimplification.utils import tree_utils

from discoursesimplification import config


class RestrictiveParticipialExtractor(ExtractionRule):
    def __init__(self):
        super().__init__()

    def extract(self, leaf: Leaf) -> Extraction:
        p = "ROOT <<: (S=s < VP=mainverb &<< (NP|PP=head <, (NP=np $+ (VP=vp [<, (ADVP|PP $+ VBG|VBN=vbgn) | <, VBG|VBN=vbgn] )) & [> (PP !> S)| > (VP > S)]))"
        matches = config.corenlp_client.tregex(leaf.text, p)

        if len(matches['sentences'][0]) > 0:
            match = matches['sentences'][0][str(0)]
            matched_node_s = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "s")
            matched_node_mainverb = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "mainverb")
            matched_node_np = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "np")
            matched_node_vp = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "vp")
            matched_node_vbgn = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "vbgn")
            matched_node_head = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "head")

            # the left, superordinate constituent
            left_constituent_words = []
            left_constituent_words.extend(
                parse_tree_extraction_utils.get_preceding_words(leaf.parse_tree, matched_node_vp, False))
            left_constituent_words.extend(
                parse_tree_extraction_utils.get_following_words(leaf.parse_tree, matched_node_vp, False))
            left_constituent = Leaf(self.__class__.__name__, None,
                                    words_utils.words_to_proper_sentence_string(left_constituent_words))

            # the right, subordinate constituent
            right_constituent_words = []
            right_constituent_words.extend(parse_tree_extraction_utils.get_containing_words(matched_node_np))
            right_constituent_words.extend(
                self.rephrase_apposition_non_res(matched_node_mainverb, matched_node_np, matched_node_vbgn))
            right_constituent_words.extend(parse_tree_extraction_utils.get_following_words(
                matched_node_head, matched_node_vbgn, False))
            right_constituent = Leaf(self.__class__.__name__, None,
                                     words_utils.words_to_proper_sentence_string(right_constituent_words))

            cue_phrase_words = parse_tree_extraction_utils.get_preceding_words(matched_node_vbgn, matched_node_s, False)
            relation = self.classifier.classify_subordinating(cue_phrase_words)
            if relation is None:
                relation = Relation.IDENTIFYING_DEFINITION

            res = Extraction(self.__class__.__name__, False, None, relation,
                             True, [left_constituent, right_constituent])

            return res

        return None
