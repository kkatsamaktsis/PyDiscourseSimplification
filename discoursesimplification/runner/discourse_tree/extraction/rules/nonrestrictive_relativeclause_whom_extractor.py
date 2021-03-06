from discoursesimplification.runner.discourse_tree.extraction.extraction import Extraction
from discoursesimplification.runner.discourse_tree.extraction.extraction_rule import ExtractionRule
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.words import words_utils
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf
from discoursesimplification.utils import tree_utils

from discoursesimplification import config


class NonRestrictiveRelativeClauseWhomExtractor(ExtractionRule):
    def __init__(self):
        super().__init__()

    def extract(self, leaf: Leaf) -> Extraction:
        p = "ROOT <<: (S << (NP=head <, NP=np & < (/,/=comma $+ (SBAR=sbar <, (WHNP $+ (S=s <, NP=np2 & <- (VP=vp ?<+(VP) PP=prep)) & <<: (WP <: whom)) & ?$+ /,/=comma2))))"
        matches = config.corenlp_client.tregex(leaf.text, p)

        if len(matches['sentences'][0]) > 0:
            match = matches['sentences'][0][str(0)]
            matched_node_comma = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "comma")
            matched_node_comma2 = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "comma2")
            matched_node_sbar = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "sbar")
            matched_node_np2 = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "np2")
            matched_node_prep = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "prep")
            matched_node_vp = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "vp")
            matched_node_np = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "np")
            matched_node_s = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "s")

            # the left, superordinate constituent
            left_constituent_words = []
            left_constituent_words.extend(
                parse_tree_extraction_utils.get_preceding_words(leaf.parse_tree, matched_node_comma, False))
            
            if matched_node_comma2 is not None:
                left_constituent_words.extend(
                    parse_tree_extraction_utils.get_following_words_numbered_node_instance(
                        leaf.parse_tree, matched_node_comma2, 2, False))
            else:
                left_constituent_words.extend(
                    parse_tree_extraction_utils.get_following_words(leaf.parse_tree, matched_node_sbar, False))
            left_constituent = Leaf(self.__class__.__name__, None,
                                    words_utils.words_to_proper_sentence_string(left_constituent_words))

            # the right, subordinate constituent
            right_constituent_words = []
            right_constituent_words.extend(parse_tree_extraction_utils.get_containing_words(matched_node_np2))
            if matched_node_prep is not None and tree_utils.get_value(matched_node_prep).split(" ")[0] == "PP":
                right_constituent_words.extend(parse_tree_extraction_utils.get_preceding_words(
                    matched_node_vp, matched_node_prep, False))
                right_constituent_words.extend(parse_tree_extraction_utils.get_containing_words(matched_node_np))
                right_constituent_words.extend(parse_tree_extraction_utils.get_containing_words(matched_node_prep))
            else:
                right_constituent_words.extend(parse_tree_extraction_utils.get_containing_words(matched_node_vp))
                right_constituent_words.extend(parse_tree_extraction_utils.get_containing_words(matched_node_np))

            right_constituent = Leaf(self.__class__.__name__, None,
                                     words_utils.words_to_proper_sentence_string(right_constituent_words))

            # relation
            cue_phrase_words = parse_tree_extraction_utils.get_preceding_words(matched_node_sbar, matched_node_s, False)
            relation = self.classifier.classify_subordinating(cue_phrase_words)
            if relation is None:
                relation = Relation.DESCRIBING_DEFINITION

            res = Extraction(self.__class__.__name__, False, cue_phrase_words, relation,
                             True, [left_constituent, right_constituent])

            return res

        return None
