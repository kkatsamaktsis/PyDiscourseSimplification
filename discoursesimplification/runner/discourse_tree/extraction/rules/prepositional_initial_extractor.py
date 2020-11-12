from discoursesimplification.runner.discourse_tree.extraction.extraction import Extraction
from discoursesimplification.runner.discourse_tree.extraction.extraction_rule import ExtractionRule
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.utils import tree_utils
from discoursesimplification.utils.ner.ner_string_parse_exception import NERStringParseException
from discoursesimplification.utils.ner.ner_string_parser import NERStringParser
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.pos.pos_tagger import POSTagger
from discoursesimplification.utils.words import words_utils
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf

from discoursesimplification import config


class PrepositionalInitialExtractor(ExtractionRule):
    def __init__(self):
        super().__init__()

    def extract(self, leaf: Leaf) -> Extraction:
        p = "ROOT <<: (S <, (PP=prep ?$+ /,/ & $++ VP=vp))"
        matches = config.corenlp_client.tregex(leaf.text, p)

        if len(matches['sentences'][0]) > 0:
            match = matches['sentences'][0][str(0)]
            matched_node_prep = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "prep")
            matched_node_vp = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "vp")

            # rephrase
            left_constituent_words = self.rephrase_enablement(matched_node_prep, matched_node_vp)
            left_constituent = Leaf(self.__class__.__name__, None,
                                    words_utils.words_to_proper_sentence_string(left_constituent_words))
            left_constituent.to_simple_context = True

            # the right, superordinate constituent
            right_constituent_words = []
            right_constituent_words.extend(parse_tree_extraction_utils.get_preceding_words(
                leaf.parse_tree, matched_node_prep, False))
            right_constituent_words.extend(parse_tree_extraction_utils.get_following_words(
                leaf.parse_tree, matched_node_prep, False))
            right_constituent = Leaf(self.__class__.__name__, None,
                                     words_utils.words_to_proper_sentence_string(right_constituent_words))
            # relation
            relation = Relation.UNKNOWN_SUBORDINATION
            pos = POSTagger.parse(left_constituent.text)
            try:
                ner = NERStringParser.parse(left_constituent.text)
                for i in range(0, len(ner.tokens)):
                    if ner.tokens[i].category == "LOCATION":
                        relation = Relation.SPATIAL
                    elif ner.tokens[i].category == "DATE":
                        relation = Relation.TEMPORAL

            except NERStringParseException:
                print("NERStringParseException")

            res = Extraction(self.__class__.__name__, False, None, relation,
                             False, [left_constituent, right_constituent])

            return res

        return None

