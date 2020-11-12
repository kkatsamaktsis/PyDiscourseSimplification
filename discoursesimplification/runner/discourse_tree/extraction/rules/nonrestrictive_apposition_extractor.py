from discoursesimplification.runner.discourse_tree.extraction.extraction import Extraction
from discoursesimplification.runner.discourse_tree.extraction.extraction_rule import ExtractionRule
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.utils.ner.ner_string_parse_exception import NERStringParseException
from discoursesimplification.utils.ner.ner_string_parser import NERStringParser
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.pos.pos_tagger import POSTagger
from discoursesimplification.utils.words import words_utils
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf
from discoursesimplification.utils import tree_utils

from discoursesimplification import config


class NonRestrictiveAppositionExtractor(ExtractionRule):
    def __init__(self):
        super().__init__()

    def extract(self, leaf: Leaf) -> Extraction:
        p = "ROOT <<: (S < VP=vp & << (NP=np1 $+ (/,/=comma $+ (NP=np2 !$ CC & ?$+ /,/=comma2))))"
        matches = config.corenlp_client.tregex(leaf.text, p)

        if len(matches['sentences'][0]) > 0:  # TODO should be loop
            match = matches['sentences'][0][str(0)]
            matched_node_vp = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "vp")
            matched_node_np1 = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "np1")
            matched_node_np2 = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "np2")
            matched_node_comma = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "comma")
            matched_node_comma2 = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "comma2")

            # the left, !subordinate! constituent
            left_constituent_words = []
            words = []
            words.extend(parse_tree_extraction_utils.get_containing_words(matched_node_np2))
            l = Leaf(self.__class__.__name__, None, words_utils.words_to_proper_sentence_string(words))
            pos = POSTagger.parse(l.text)

            t1 = matched_node_np1
            t2 = matched_node_np2
            entity1 = False
            entity2 = False

            try:
                ner1 = NERStringParser.parse_tree_parse(t1)
                ner2 = NERStringParser.parse_tree_parse(t2)

                loc1 = False
                loc2 = False

                for i in range(0, len(ner1.get_words())):
                    if ner1.tokens[i].category == "PERSON" or ner1.tokens[i].category == "ORGANIZATION":
                        entity1 = True
                        break
                    if ner1.tokens[i].category == "LOCATION":
                        loc1 = True
                        break

                for i in range(0, len(ner2.get_words())):
                    if ner2.tokens[i].category == "PERSON" or ner2.tokens[i].category == "ORGANIZATION":
                        entity2 = True
                        break
                    if ner2.tokens[i].category == "LOCATION":
                        loc2 = True
                        break

                if loc1 and loc2:
                    pass  # TODO should be: continue

            except NERStringParseException:
                print("NERStringParseException")

            if entity1:
                left_constituent_words.extend(parse_tree_extraction_utils.get_containing_words(matched_node_np1))
                left_constituent_words.extend(
                    self.rephrase_apposition_non_res(matched_node_vp, matched_node_np1, matched_node_np2))
            elif entity2:
                left_constituent_words.extend(parse_tree_extraction_utils.get_containing_words(matched_node_np2))
                left_constituent_words.extend(
                    self.rephrase_apposition_non_res(matched_node_vp, matched_node_np2, matched_node_np1))
            else:
                left_constituent_words.extend(parse_tree_extraction_utils.get_containing_words(matched_node_np1))
                left_constituent_words.extend(
                    self.rephrase_apposition_non_res(matched_node_vp, matched_node_np1, matched_node_np2))

            left_constituent = Leaf(self.__class__.__name__, None,
                                    words_utils.words_to_proper_sentence_string(left_constituent_words))

            # the right, superordinate constituent
            right_constituent_words = []
            right_constituent_words.extend(parse_tree_extraction_utils.get_preceding_words(
                leaf.parse_tree, matched_node_comma, False))
            if matched_node_comma2 is not None:
                right_constituent_words.extend(parse_tree_extraction_utils.get_following_words_numbered_node_instance(
                    leaf.parse_tree, matched_node_comma2, 2, False))
            else:
                right_constituent_words.extend(parse_tree_extraction_utils.get_following_words(
                    leaf.parse_tree, matched_node_np2, False))

            right_constituent = Leaf(self.__class__.__name__, None,
                                     words_utils.words_to_proper_sentence_string(right_constituent_words))

            # relation
            relation = Relation.ELABORATION

            res = Extraction(self.__class__.__name__, False, None, relation,
                             False, [left_constituent, right_constituent])

            return res

        return None
