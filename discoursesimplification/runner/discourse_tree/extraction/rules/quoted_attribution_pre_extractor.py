from discoursesimplification.runner.discourse_tree.extraction.extraction import Extraction
from discoursesimplification.runner.discourse_tree.extraction.extraction_rule import ExtractionRule
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.words import words_utils
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf
from discoursesimplification.utils import tree_utils

from discoursesimplification import config


class QuotedAttributionPreExtractor(ExtractionRule):
    def __init__(self):
        super().__init__()

    def extract(self, leaf: Leaf) -> Extraction:
        p = "ROOT <<: (S < (S|SBAR|SBARQ [,, /``/=start | <<, /``/=start] [.. /''/=end | <<- /''/=end] $.. (NP=np [$,, VP=vpb | $.. VP=vpa])))"
        matches = config.corenlp_client.tregex(leaf.text, p)

        if len(matches['sentences'][0]) > 0:
            match = matches['sentences'][0][str(0)]
            matched_node_start = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "start")
            matched_node_end = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "end")
            matched_node_np = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "np")
            matched_node_vpa = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "vpa")
            matched_node_vpb = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "vpb")

            quote_start = matched_node_start
            quote_end = matched_node_end

            # the left, superordinate constituent
            left_constituent_words = parse_tree_extraction_utils.get_words_in_between(
                leaf.parse_tree, quote_start, quote_end, False, False)
            left_constituent = Leaf(self.__class__.__name__, None,
                                    words_utils.words_to_proper_sentence_string(left_constituent_words))

            # the right, subordinate constituent
            right_constituent_words = []
            right_constituent_words.extend(parse_tree_extraction_utils.get_preceding_words(
                leaf.parse_tree, quote_start, False))
            right_constituent_words.extend(parse_tree_extraction_utils.get_containing_words(matched_node_np))
            if matched_node_vpb is not None:
                right_constituent_words.extend(parse_tree_extraction_utils.get_containing_words(matched_node_vpb))
                right_constituent_words.extend(parse_tree_extraction_utils.get_following_words(
                    leaf.parse_tree, matched_node_np, False))
            else:
                right_constituent_words.extend(parse_tree_extraction_utils.get_containing_words(matched_node_vpa))
                right_constituent_words.extend(parse_tree_extraction_utils.get_following_words(
                    leaf.parse_tree, matched_node_vpa, False))

            # rephrase
            right_constituent_words = self.rephrase_intra_sentential_attribution(right_constituent_words)
            right_constituent = Leaf(self.__class__.__name__, None,
                                     words_utils.words_to_proper_sentence_string(right_constituent_words))
            right_constituent.allow_split = False
            right_constituent.to_simple_context = True

            # relation
            head_verb = None
            if matched_node_vpb is not None:
                head_verb = self.get_head_verb(matched_node_vpb)
            else:
                head_verb = self.get_head_verb(matched_node_vpa)

            # only extract if verb matches
            if head_verb is not None and self.classifier.check_attribution(head_verb):
                relation = Relation.ATTRIBUTION

                res = Extraction(self.__class__.__name__, False, None, relation,
                                 True, [left_constituent, right_constituent])

                return res

        return None
