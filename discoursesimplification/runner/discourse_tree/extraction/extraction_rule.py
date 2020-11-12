from typing import List
from enum import Enum

from discoursesimplification.runner.discourse_tree.classification.cue_phrase_classifier import CuePhraseClassifier
from discoursesimplification.runner.discourse_tree.extraction.extraction import Extraction
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.parse_tree.parse_tree_exception import ParseTreeException
from discoursesimplification.utils.parse_tree.parse_tree_parser import ParseTreeParser
from discoursesimplification.utils import tree_utils

from discoursesimplification import config
from discoursesimplification.utils.words import words_utils
from nltk.tree import Tree

class Tense(Enum):
    PRESENT = "PRESENT"
    PAST = "PAST"


class Number(Enum):
    SINGULAR = "SINGULAR"
    PLURAL = "PLURAL"


# This class is meant to be "abstract"
class ExtractionRule:
    def __init__(self):
        self.classifier = CuePhraseClassifier()

    def extract(self, leaf: Leaf) -> Extraction:
        pass  # Implemented in subclasses

    @staticmethod
    def get_siblings(parse_tree: Tree, tags: List[str]):
        # child[0] will always be "S". Get its children which will be the siblings
        # parse_tree = parse_tree[0]
        return list(filter(lambda c: tree_utils.get_value(c) in tags,
                           [child for child in parse_tree] if isinstance(parse_tree, list) else parse_tree))

    @staticmethod
    def get_number(np) -> Number:
        res = Number.SINGULAR

        # find plural forms
        p = "NNS|NNPS"
        # Get the words in the tree as a single str
        np_str = words_utils.words_to_string(parse_tree_extraction_utils.yield_words(np, []))
        matches = config.corenlp_client.tregex(np_str, p)
        if len(matches['sentences'][0]) > 0:
            res = Number.PLURAL

        # find and
        p = "CC <<: and"
        matches = config.corenlp_client.tregex(np_str, p)
        if len(matches['sentences'][0]) > 0:
            res = Number.PLURAL

        return res

    @staticmethod
    def get_tense(vp) -> Tense:
        res = Tense.PRESENT

        # find past tense
        p = "VBD|VBN"
        # Get the words in the tree as a single str
        vp_str = words_utils.words_to_string(parse_tree_extraction_utils.yield_words(vp, []))

        matches = config.corenlp_client.tregex(vp_str, p)

        if len(matches['sentences'][0]) > 0:
            res = Tense.PAST

        return res

    @staticmethod
    def get_head_verb(vp: Tree):
        pattern = tree_utils.get_value(vp) + " [ <+(VP) (VP=lowestvp !< VP < /V../=v) | ==(VP=lowestvp !< VP < /V../=v) ]"
        vp_str = words_utils.words_to_string(parse_tree_extraction_utils.yield_words(vp, []))
        matches = config.corenlp_client.tregex(vp_str, pattern)
        if len(matches['sentences'][0]) > 0:
            match = matches['sentences'][0][str(0)]
            matched_node_v = tree_utils.matcher_get_node_from_tree(vp, match, "v")
            return parse_tree_extraction_utils.get_containing_words(matched_node_v)[0]

        return None

    @staticmethod
    def append_words_from_tree(words: List[str], tree: Tree) -> List[str]:
        res = []
        res.extend(words)

        p = tree_utils.get_value(tree) + " <<, NNP|NNPS"
        # Get the words in the tree as a single str
        tree_str = words_utils.words_to_string(parse_tree_extraction_utils.yield_words(tree, []))

        matches = config.corenlp_client.tregex(tree_str, p)

        is_first = True
        for word in parse_tree_extraction_utils.yield_words(tree, []):
            if is_first and len(matches['sentences'][0]) == 0:
                res.append(words_utils.lowercase_word(word))
            else:
                res.append(word)
            is_first = False

        return res

    @staticmethod
    def rephrase_intra_sentential_attribution(words: List[str]) -> List[str]:
        try:
            res = []

            parse_tree = ParseTreeParser.parse(words_utils.words_to_proper_sentence_string(words))
            parse_tree_str = words_utils.words_to_proper_sentence_string(words)

            p = "ROOT << (S !> S < (NP=np ?$,, PP=pp $.. VP=vp))"
            matches = config.corenlp_client.tregex(parse_tree_str, p)
            if len(matches['sentences'][0]) > 0:
                match = matches['sentences'][0][str(0)]
                pp = tree_utils.matcher_get_node_from_tree(parse_tree, match, "pp")  # optional
                np = tree_utils.matcher_get_node_from_tree(parse_tree, match, "np")
                vp = tree_utils.matcher_get_node_from_tree(parse_tree, match, "vp")

                tense = ExtractionRule.get_tense(vp)
                if tense == Tense.PRESENT:
                    res.append("This")
                    res.append("is")
                    res.append("what")
                else:
                    res.append("This")
                    res.append("was")
                    res.append("what")
                res = ExtractionRule.append_words_from_tree(res, np)
                res = ExtractionRule.append_words_from_tree(res, vp)
                if pp is not None:
                    res = ExtractionRule.append_words_from_tree(res, pp)

            return res
        except ParseTreeException:
            return words

    @staticmethod
    def rephrase_enablement(s, vp):
        res = []

        tense = ExtractionRule.get_tense(vp)

        if tense == Tense.PRESENT:
            res.append("This")
            res.append("is")
        else:
            res.append("This")
            res.append("was")
        res = ExtractionRule.append_words_from_tree(res, s)

        return res

    @staticmethod
    def rephrase_apposition(vp, np: str) -> str:
        res = ""

        tense = ExtractionRule.get_tense(vp)
        if tense == Tense.PRESENT:
            if np == "NN" or np == "NNP":
                res = " is "
            else:
                res = " are "
        else:
            if np == "NN" or np == "NNP":
                res = " was "
            else:
                res = " were "

        return res

    @staticmethod
    def rephrase_apposition_non_res(vp: Tree, np: Tree, np2: Tree):
        res = []

        tense = ExtractionRule.get_tense(vp)
        number = ExtractionRule.get_number(np)
        if tense == Tense.PRESENT:
            if number == Number.SINGULAR:
                res.append("is")
            else:
                res.append("are")
        else:
            if number == Number.SINGULAR:
                res.append("was")
            else:
                res.append("were")

        res = ExtractionRule.append_words_from_tree(res, np2)

        return res

    @staticmethod
    def get_rephrased_participal_s(np: Tree, vp: Tree, s: Tree, vbgn: Tree):
        number = ExtractionRule.get_number(np)
        tense = ExtractionRule.get_tense(vp)

        p = vbgn.label() + " <<: (having . (been . VBN=vbn))"
        p2 = vbgn.label() + " <<: (having . VBN=vbn)"
        p3 = vbgn.label() + " <<: (being . VBN=vbn)"

        # Get the words in the tree as a single str
        s_str = words_utils.words_to_string(parse_tree_extraction_utils.yield_words(s, []))
        matches = config.corenlp_client.tregex(s_str, p)
        if len(matches['sentences'][0]) > 0:
            match = matches['sentences'][0][str(0)]
            matched_node_vbn = tree_utils.matcher_get_node_from_tree(s, match, "vbn")
            res = []

            res.append("has" if number == Number.SINGULAR else "have")
            res.append("been")
            next_words = parse_tree_extraction_utils.get_following_words(s, matched_node_vbn, True)
            if len(next_words) > 0:
                next_words[0] = words_utils.lowercase_word(next_words[0])
            res.extend(next_words)

            return res

        matches = config.corenlp_client.tregex(s_str, p2)
        if len(matches['sentences'][0]) > 0:
            match = matches['sentences'][0][str(0)]
            matched_node_vbn = tree_utils.matcher_get_node_from_tree(s, match, "vbn")
            res = []

            res.append("has" if number == Number.SINGULAR else "have")
            next_words = parse_tree_extraction_utils.get_following_words(s, matched_node_vbn, True)
            if len(next_words) > 0:
                next_words[0] = words_utils.lowercase_word(next_words[0])
            res.extend(next_words)

            return res

        matches = config.corenlp_client.tregex(s_str, p3)
        if len(matches['sentences'][0]) > 0:
            match = matches['sentences'][0][str(0)]
            matched_node_vbn = tree_utils.matcher_get_node_from_tree(s, match, "vbn")
            res = []

            if tense == Tense.PRESENT:
                res.append("is" if number == Number.SINGULAR else "are")
            else:
                res.append("was" if number == Number.SINGULAR else "were")

            next_words = parse_tree_extraction_utils.get_following_words(s, matched_node_vbn, True)
            if len(next_words) > 0:
                next_words[0] = words_utils.lowercase_word(next_words[0])
            res.extend(next_words)

            return res

        # default
        res = []
        if tense == Tense.PRESENT:
            res.append("is" if number == Number.SINGULAR else "are")
        else:
            res.append("was" if number == Number.SINGULAR else "were")
        next_words = parse_tree_extraction_utils.get_following_words(s, vbgn, True)
        if len(next_words) > 0:
            next_words[0] = words_utils.lowercase_word(next_words[0])
        res.extend(next_words)

        return res

