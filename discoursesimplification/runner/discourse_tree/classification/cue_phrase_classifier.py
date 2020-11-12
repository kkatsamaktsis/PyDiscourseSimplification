from typing import List

from discoursesimplification.config import Config
from discoursesimplification.runner.discourse_tree import relation_utility
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.utils.words import words_utils
import re


class Mapping:
    def __init__(self, relation: Relation, cue_phrase_pattern: str, contain: bool):
        self.relation = relation
        self.cue_phrase_pattern = "^(?i:" + (".*?" if contain else "") + "(?<!\\w)" + cue_phrase_pattern + "(?!\\w)" \
                                  + (".*?" if contain else "") + ")$"
        self.cue_phrase_pattern_size = len(cue_phrase_pattern)

    def check(self, cue_phrase: str) -> bool:
        return bool(re.match(self.cue_phrase_pattern, cue_phrase))


class CuePhraseClassifier:
    def __init__(self):
        # load attribution verbs
        self.attribution_verbs = []
        for verb in Config.attribution_verbs:
            self.attribution_verbs.append(verb)

        # load patterns
        self.coordinating_phrases = []
        coordinating_contain_matching = Config.cue_phrases['coordinating_phrases']['matching'] == "contained"
        for (pattern, relation) in Config.cue_phrases['coordinating_phrases']['phrases']:
            relation = relation_utility.str_to_relation(relation)
            self.coordinating_phrases.append(Mapping(relation, pattern, coordinating_contain_matching))

        self.subordinating_phrases = []
        subordinating_contain_matching = Config.cue_phrases['subordinating_phrases']['matching'] == "contained"
        for (pattern, relation) in Config.cue_phrases['subordinating_phrases']['phrases']:
            relation = relation_utility.str_to_relation(relation)
            self.subordinating_phrases.append(Mapping(relation, pattern, subordinating_contain_matching))

        self.adverbial_phrases = []
        adverbial_contain_matching = Config.cue_phrases['adverbial_phrases']['matching'] == "contained"
        for (pattern, relation) in Config.cue_phrases['adverbial_phrases']['phrases']:
            relation = relation_utility.str_to_relation(relation)
            self.adverbial_phrases.append(Mapping(relation, pattern, adverbial_contain_matching))

    def classify(self, mappings, cue_phrase: str):
        if len(cue_phrase) == 0:
            return None

        best_mapping = None
        for mapping in mappings:
            if mapping.check(cue_phrase):
                if not(best_mapping is not None):
                    best_mapping = mapping
                elif mapping.cue_phrase_pattern_size >= best_mapping.cue_phrase_pattern_size:
                    best_mapping = mapping

        return best_mapping.relation if best_mapping is not None else None

    def classify_coordinating(self, cue_phrase_words: str):
        if isinstance(cue_phrase_words, List):
            cue_phrase_words = words_utils.words_to_string(cue_phrase_words)  # convert the list to string
        return self.classify(self.coordinating_phrases, cue_phrase_words)

    def classify_subordinating(self, cue_phrase_words):
        if isinstance(cue_phrase_words, List):
            cue_phrase_words = words_utils.words_to_string(cue_phrase_words)  # convert the list to string
        return self.classify(self.subordinating_phrases, cue_phrase_words)

    def classify_adverbial(self, cue_phrase_words):
        if isinstance(cue_phrase_words, List):
            cue_phrase_words = words_utils.words_to_string(cue_phrase_words)  # convert the list to string
        return self.classify(self.adverbial_phrases, cue_phrase_words)

    def check_attribution(self, cue_phrase_words):
        if not isinstance(cue_phrase_words, List):
            cue_phrase_words = [cue_phrase_words]  # make list from string

        for word in cue_phrase_words:
            if words_utils.lemmatize(word).lower() in self.attribution_verbs:
                return True

        return False
