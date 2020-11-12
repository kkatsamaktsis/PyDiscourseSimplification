from discoursesimplification.runner.discourse_tree.extraction.extraction import Extraction
from discoursesimplification.runner.discourse_tree.extraction.extraction_rule import ExtractionRule
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.words import words_utils
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf
from discoursesimplification.utils import tree_utils

from discoursesimplification import config


class QuotedAttributionPostExtractor(ExtractionRule):
    def __init__(self):
        super().__init__()

    def extract(self, leaf: Leaf) -> Extraction:
        p = "ROOT <<: (S < (NP $.. (VP=vp <+(VP) (SBAR=sbar [,, /``/=start | <<, /``/=start] [.. /''/=end | <<- /''/=end]))))"
        matches = config.corenlp_client.tregex(leaf.text, p)

        if len(matches['sentences'][0]) > 0:
            match = matches['sentences'][0][str(0)]
            matched_node_start = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "start")
            matched_node_end = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "end")
            matched_node_vp = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "vp")

            quote_start = matched_node_start
            quote_end = matched_node_end

            # the left, subordinate constituent
            left_constituent_words = []
            left_constituent_words.extend(parse_tree_extraction_utils.get_preceding_words(
                leaf.parse_tree, quote_start, False))
            left_constituent_words.extend(parse_tree_extraction_utils.get_following_words(
                leaf.parse_tree, quote_end, False))

            # rephrase
            left_constituent_words = self.rephrase_intra_sentential_attribution(left_constituent_words)
            left_constituent = Leaf(self.__class__.__name__, None,
                                    words_utils.words_to_proper_sentence_string(left_constituent_words))
            left_constituent.allow_split = False
            left_constituent.to_simple_context = True

            # the right, superordinate constituent
            right_constituent_words = parse_tree_extraction_utils.get_words_in_between(
                leaf.parse_tree, quote_start, quote_end, False, False)
            right_constituent = Leaf(self.__class__.__name__, None,
                                     words_utils.words_to_proper_sentence_string(right_constituent_words))

            # relation
            head_verb = self.get_head_verb(matched_node_vp)

            # only extract if verb matches
            if head_verb is not None and self.classifier.check_attribution(head_verb):
                relation = Relation.ATTRIBUTION

                res = Extraction(self.__class__.__name__, False, None, relation,
                                 False, [left_constituent, right_constituent])

                return res

        return None
