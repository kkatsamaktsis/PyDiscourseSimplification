from __future__ import annotations

from typing import List

from discoursesimplification.utils.ner.ner_string import NERString
from discoursesimplification.utils.ner.tner.tner_token import TNERToken


class TNERString(NERString):
    def __init__(self, tokens: List[TNERToken], parse_tree):
        super().__init__(list(tokens))
        self.parse_tree = parse_tree
        for t in self.tokens:
            t.set_ner_string(self)
