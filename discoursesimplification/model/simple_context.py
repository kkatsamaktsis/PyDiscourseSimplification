import re

from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.parse_tree.parse_tree_exception import ParseTreeException
from discoursesimplification.utils.parse_tree.parse_tree_parser import ParseTreeParser
from discoursesimplification.utils.words import words_utils


class SimpleContext:
    __PHRASE_PATTERN = re.compile("^\\W*this\\W+\\w+\\W+(?P<phrase>.*\\w+.*)$", re.IGNORECASE)
    __ATTRIBUTION_PHRASE_PATTERN = re.compile("^\\W*this\\W+\\w+\\W+what\\W+(?P<phrase>.*\\w+.*)$", re.IGNORECASE)

    def __init__(self, parse_tree: any):
        self.parse_tree = parse_tree
        self.relation = Relation.UNKNOWN
        self.time_information = None
        self.text = words_utils.words_to_string(parse_tree_extraction_utils.get_containing_words(self.parse_tree))
        self.__extract_phrase()

    def set_parse_tree(self, parse_tree: any):
        self.parse_tree = parse_tree
        self.__extract_phrase()

    def __extract_phrase(self):
        self.phrase = self.parse_tree

        matched = False

        if self.relation == Relation.ATTRIBUTION:
            pattern = SimpleContext.__ATTRIBUTION_PHRASE_PATTERN
            matches = list(re.finditer(pattern, self.text))
            if len(matches) > 0:
                try:
                    self.phrase = ParseTreeParser.parse(matches[0].groupdict()['phrase'])
                    matched = True
                except ParseTreeException:
                    pass
        else:
            pattern = SimpleContext.__PHRASE_PATTERN
            matches = list(re.finditer(pattern, self.text))
            if len(matches) > 0:
                try:
                    self.phrase = ParseTreeParser.parse(matches[0].groupdict()['phrase'])
                    matched = True
                except ParseTreeException:
                    pass

        if not matched:
            self.relation = Relation.NOUN_BASED

        self.phrase_text = self.get_phrase_text()

    def get_phrase_text(self):
        return words_utils.words_to_string(parse_tree_extraction_utils.get_containing_words(self.phrase))

    def set_relation(self, relation: Relation):
        self.relation = relation
        self.__extract_phrase()
