from __future__ import annotations

from typing import List

from discoursesimplification.utils.ner.ner_token import NERToken
from discoursesimplification.utils.ner.ner_token_group import NERTokenGroup


class NERString:
    def __init__(self, tokens: List[NERToken]):
        self.tokens = tokens
        self.groups = None  # to be set by create_groups()
        self.create_groups()

    def create_groups(self):
        self.groups = []

        last_category = None
        curr_group_tokens = []
        for ner_token in self.tokens:

            if last_category is not None and not(ner_token.category == last_category):
                # add
                self.groups.append(NERTokenGroup(curr_group_tokens))
                curr_group_tokens = []

            curr_group_tokens.append(ner_token)
            last_category = ner_token.category

        # add
        self.groups.append(NERTokenGroup(curr_group_tokens))

    def get_words(self, from_index: int = None, to_index: int = None):
        if from_index is None and to_index is None:
            from_index = 0
            to_index = len(self.tokens)
        return list(map(lambda t: t.text, self.tokens[from_index:to_index]))

    def __str__(self):
        return "\n".join(list(map(lambda t: str(t), self.tokens)))

    def __repr__(self):
        return self.__str__()
