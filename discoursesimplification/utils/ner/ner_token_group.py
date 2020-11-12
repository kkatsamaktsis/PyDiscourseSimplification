from __future__ import annotations

from typing import List

from discoursesimplification.utils.ner import ner_extraction_utils
from discoursesimplification.utils.ner.ner_token import NERToken


class NERTokenGroup:
    def __init__(self, tokens: List[NERToken]):
        self.tokens = tokens

    def get_from_token_index(self):
        return self.tokens[0].index

    def get_to_token_index(self):
        return self.tokens[len(self.tokens) - 1].index

    def get_category(self):
        return self.tokens[0].category

    def is_named_entity(self) -> bool:
        return not(self.get_category() == ner_extraction_utils.NO_CATEGORY)

    def get_words(self):
        return list(map(lambda t: t.text, self.tokens))

    def __str__(self):
        return "[\n" + ("\n".join(list(map(lambda t: str(t), self.tokens)))) + "\n]"

    def __repr__(self):
        return self.__str__()
