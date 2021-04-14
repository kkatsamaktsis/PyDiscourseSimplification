from __future__ import annotations

from discoursesimplification import config
from discoursesimplification.utils import tree_utils
from discoursesimplification.utils.ner.ner_string import NERString
from discoursesimplification.utils.ner.ner_string_parse_exception import NERStringParseException
from discoursesimplification.utils.ner.ner_token import NERToken
from discoursesimplification.utils.ner.tner.tner_string import TNERString
from discoursesimplification.utils.ner.tner.tner_token import TNERToken
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.words import words_utils


class NERStringParser:
    @staticmethod
    def parse(text: str) -> NERString:
        tokens = []

        ann = config.corenlp_client.annotate(text, annotators=['tokenize', 'ssplit', 'ner'])
        sentence = ann.sentence[0]

        idx = 0
        for token in sentence.token:
            # create text
            txt = token.value
            category = token.ner
            token = NERToken(idx, txt, category)
            tokens.append(token)

            idx += 1

        return NERString(tokens)

    @staticmethod
    def parse_tree_parse(parse_tree) -> TNERString:
        tokens = []

        parse_tree_leaf_numbers = parse_tree_extraction_utils.get_leaf_numbers(parse_tree, parse_tree)

        ann = config.corenlp_client.annotate(words_utils.words_to_string(
            parse_tree_extraction_utils.yield_words(parse_tree, [])), annotators=['tokenize', 'ssplit', 'ner'])

        sentence = ann.sentence[0]

        if len(parse_tree_leaf_numbers) != len(sentence.token):
            raise NERStringParseException("Could not map NER string to parseTree")

        idx = 0
        for ner_token in sentence.token:
            # create token
            text = ner_token.value
            category = ner_token.ner
            token = TNERToken(idx, text, category, tree_utils.get_node_number(parse_tree, parse_tree_leaf_numbers[idx]))
            tokens.append(token)

            idx += 1

        return TNERString(tokens, parse_tree)
