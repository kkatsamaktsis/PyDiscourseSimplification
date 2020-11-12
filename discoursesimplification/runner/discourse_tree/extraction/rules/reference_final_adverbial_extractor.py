from discoursesimplification.runner.discourse_tree.extraction.extraction import Extraction
from discoursesimplification.runner.discourse_tree.extraction.extraction_rule import ExtractionRule
from discoursesimplification.utils.parse_tree import parse_tree_extraction_utils
from discoursesimplification.utils.words import words_utils
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf
from discoursesimplification.utils import tree_utils

from discoursesimplification import config


class ReferenceFinalAdverbialExtractor(ExtractionRule):
    def __init__(self):
        super().__init__()

    def extract(self, leaf: Leaf) -> Extraction:
        p = "ROOT <<: (S=s < (VP <+(VP) (ADVP|PP=adv))) : (=s [<<- =adv | <<- (/\\./ , =adv)])"
        matches = config.corenlp_client.tregex(leaf.text, p)

        if len(matches['sentences'][0]) > 0:  # Should be loop
            match = matches['sentences'][0][str(0)]
            matched_node_adv = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match, "adv")

            cue_phrase_words = parse_tree_extraction_utils.get_containing_words(matched_node_adv)

            # the right constituent
            words = []
            words.extend(parse_tree_extraction_utils.get_preceding_words(leaf.parse_tree, matched_node_adv, False))
            words.extend(parse_tree_extraction_utils.get_following_words(leaf.parse_tree, matched_node_adv, False))
            right_constituent = Leaf(self.__class__.__name__, None, words_utils.words_to_proper_sentence_string(words))

            # relation
            relation = self.classifier.classify_adverbial(cue_phrase_words)

            # only if present
            if relation is not None:
                res = Extraction(self.__class__.__name__, True, cue_phrase_words, relation, True, [right_constituent])

                return res

        return None
