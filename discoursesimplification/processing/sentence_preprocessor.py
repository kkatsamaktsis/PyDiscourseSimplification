import re

from discoursesimplification.config import Config

ROUND_BRACKET_PATTERN = "\\([^\\(\\)]*?\\)"
SQUARE_BRACKET_PATTERN = "\\[[^\\[\\]]*?\\]"
CURLY_BRACKET_PATTERN = "\\{[^\\{\\}]*?\\}"

ROUND_BRACKET_PATTERN2 = "-LRB-((?!-LRB-|-RRB-).)*?-RRB-"
SQUARE_BRACKET_PATTERN2 = "-LSB-((?!-LSB-|-RSB-).)*?-RSB-"
CURLY_BRACKET_PATTERN2 = "-LCB-((?!-LCB-|-RCB-).)*?-RCB-"

WHITESPACE_PATTERN = "\\s+"

bracket_patterns = [ROUND_BRACKET_PATTERN, SQUARE_BRACKET_PATTERN, CURLY_BRACKET_PATTERN,
                    ROUND_BRACKET_PATTERN2, SQUARE_BRACKET_PATTERN2, CURLY_BRACKET_PATTERN2]


class SentencePreprocessor:
    def __init__(self):
        self.remove_brackets = Config.sentence_preprocessor_remove_brackets

    def preprocess_sentence(self, sentence: str):
        res = sentence

        if self.remove_brackets:
            for pattern in bracket_patterns:
                res = re.sub(pattern, "", res)

        res = re.sub(WHITESPACE_PATTERN, " ", res)
        return res
