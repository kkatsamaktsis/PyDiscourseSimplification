import re

from discoursesimplification.runner.discourse_tree.extraction.extraction import Extraction
from discoursesimplification.runner.discourse_tree.extraction.extraction_rule import ExtractionRule
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.utils.ner.ner_string_parse_exception import NERStringParseException
from discoursesimplification.utils.ner.ner_string_parser import NERStringParser
from discoursesimplification.utils.parse_tree.parse_tree_parser import ParseTreeParser
from discoursesimplification.utils.pos.pos_tagger import POSTagger
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf
from discoursesimplification.utils import tree_utils

from discoursesimplification import config


class RestrictiveAppositionExtractor(ExtractionRule):
    def __init__(self):
        super().__init__()

    def extract(self, leaf: Leaf) -> Extraction:
        t = leaf.parse_tree

        try:
            ner = NERStringParser.parse_tree_parse(t)
            pattern = re.compile("(((PRP\\$|DT)\\s)*(JJ\\s)*((NN|NNS|NNP|NNPS)\\s))+(((CC|IN)\\s)((PRP\\$|DT)\\s)*(JJ\\s)*((NN|NNS|NNP|NNPS)\\s))*STOP")
            pos = POSTagger.parse(leaf.text)

            for i in range(1, len(ner.get_words())):

                if ((ner.tokens[i].category == "PERSON" and not ner.tokens[i-1].category == "PERSON")\
                        or ner.tokens[i].category == "ORGANIZATION" and not ner.tokens[i-1].category == "ORGANIZATION"
                        or ner.tokens[i].category == "LOCATION" and not ner.tokens[i-1].category == "LOCATION"):
                    po = pos[i]
                    number = po.pos

                    n = i + 1
                    attach = ner.tokens[i].text
                    while n < len(ner.tokens) \
                            and (ner.tokens[n].category == "PERSON"
                                 or ner.tokens[n].category == "ORGANIZATION"
                                 or ner.tokens[n].category == "LOCATION"):
                        attach = attach + ' ' + ner.tokens[n].text
                        n += 1

                    pos_string = ""
                    text = ""
                    for j in range(0, i):
                        pos_string = pos_string + ' ' + pos[j].pos
                        text = text + ' ' + pos[j].text
                    pos_string = pos_string + ' ' + "STOP"

                    for match in pattern.finditer(pos_string):
                        m = match.group().split(" ")
                        appos = ""
                        a = text.split(" ")
                        for k in range(0, len(m) - 1):
                            appos = a[len(a) - 1 - k] + ' ' + appos

                        p = "ROOT <<: (S < VP=vp)"
                        matches_tree = config.corenlp_client.tregex(leaf.text, p)
                        if len(matches_tree['sentences'][0]) > 0:
                            match_tree = matches_tree['sentences'][0][str(0)]
                            matched_node_vp = tree_utils.matcher_get_node_from_tree(leaf.parse_tree, match_tree, "vp")

                            apposition = ""
                            if not (appos == ""):
                                apposition = attach + self.rephrase_apposition(matched_node_vp, number) + appos + "."

                            rest = leaf.text.replace(appos, "")
                            app_tree = ParseTreeParser.parse(apposition)
                            left_constituent = Leaf(self.__class__.__name__, app_tree)

                            rest_tree = ParseTreeParser.parse(rest)
                            right_constituent = Leaf(self.__class__.__name__, rest_tree)

                            relation = Relation.ELABORATION

                            res = Extraction(self.__class__.__name__, False, None, relation,
                                             False, [left_constituent, right_constituent])

                            return res

        except NERStringParseException:
            print("NERStringParseException")

        return None
