from typing import List

from discoursesimplification import config
from discoursesimplification.utils.pos.pos_token import POSToken


class POSTagger:

    @staticmethod
    def parse(text: str) -> List[POSToken]:
        tokens = []

        ann = config.corenlp_client.annotate(text, annotators=['tokenize', 'ssplit', 'pos'])
        sentence = ann.sentence[0]

        idx = 0
        for token in sentence.token:
            # create text
            txt = token.value
            pos = token.pos
            token = POSToken(idx, txt, pos)
            tokens.append(token)

            idx += 1

        return tokens
