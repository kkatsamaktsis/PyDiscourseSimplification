from discoursesimplification.runner.discourse_tree.extraction.extraction import Extraction
from discoursesimplification.runner.discourse_tree.extraction.extraction_rule import ExtractionRule
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.parse_tree.parse_tree_parser import ParseTreeParser
from discoursesimplification.utils.words import words_utils
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf

from discoursesimplification import config


class CoordinationExtractor(ExtractionRule):
    def __init__(self):
        super().__init__()

    # @staticmethod
    # def is_npvp_clause(s):
    #    pattern = "S" + "< (NP $.. VP)"
    #    matches = config.corenlp_client.tregex(s, pattern)
    #    return print(matches['sentences'][0]['0']['match'])

    def extract(self, leaf: Leaf) -> Extraction:
        p = "ROOT <<: (S=s < (S $.. S))"
        matches = config.corenlp_client.tregex(leaf.text, p)

        if len(matches['sentences'][0]) > 0:  # range(0, len(matches['sentences'][0])):
            match = matches['sentences'][0][str(0)]
            siblings = self.get_siblings(ParseTreeParser.parse(match['namedNodes'][0]['s']['spanString']), ["S"])

            if len(siblings) >= 2:
                # constituents
                preceding_words = parse_tree_extraction_utils.get_preceding_words(leaf.parse_tree, siblings[0], False)
                following_words = parse_tree_extraction_utils.get_following_words(leaf.parse_tree, siblings[len(siblings) - 1], False)

                constituents = []
                for sibling in siblings:
                    words = []
                    words.extend(preceding_words)
                    words.extend(parse_tree_extraction_utils.get_containing_words(sibling))
                    words.extend(following_words)

                    constituent = Leaf(self.__class__.__name__, None,
                                       words_utils.words_to_proper_sentence_string(words))

                    constituents.append(constituent)

                cue_phrase_words = None
                relation = Relation.UNKNOWN_COORDINATION
                if len(constituents) == 2:
                    cue_phrase_words = parse_tree_extraction_utils.get_words_in_between(leaf.parse_tree, siblings[0],
                                                                                        siblings[len(siblings) - 1],
                                                                                        False, False)
                    relation = self.classifier.classify_coordinating(cue_phrase_words)
                    if relation is None:
                        relation = Relation.UNKNOWN_COORDINATION

                res = Extraction(self.__class__.__name__, False, cue_phrase_words, relation, True, constituents)

                return res

        return None

