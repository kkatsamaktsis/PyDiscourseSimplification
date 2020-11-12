import importlib
import logging
import logging.config

from discoursesimplification.config import Config
from discoursesimplification.processing.sentence_preprocessor import SentencePreprocessor
from discoursesimplification.runner.discourse_tree.model.coordination import Coordination
from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.runner.discourse_tree.model.sentence_leaf import SentenceLeaf
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf
from discoursesimplification.runner.discourse_tree.model.discourse_tree import DiscourseTree
from discoursesimplification.runner.discourse_tree.model.subordination import Subordination
from discoursesimplification.utils.parse_tree import parse_tree_visualizer


class DiscourseTreeCreator:

    def __init__(self, preprocessor: SentencePreprocessor):
        self.logger = logging.getLogger(__name__)

        self.preprocessor = preprocessor
        self.discourse_tree = Coordination("ROOT", Relation.UNKNOWN_COORDINATION, None, [])

        # create rules from config
        self.rules = []
        for rule in Config.rules:
            rule_mod = importlib.import_module("discoursesimplification." + rule[0])
            rule_class_ = getattr(rule_mod, rule[1])
            rule_instance = rule_class_()
            self.rules.append(rule_instance)

        self.reset()

    def reset(self):
        self.discourse_tree = Coordination("ROOT", Relation.UNKNOWN_COORDINATION, None, [])

    def add_sentence(self, sentence: str, sentence_index: int):
        preprocessed_sentence = self.preprocessor.preprocess_sentence(sentence)
        self.discourse_tree.add_coordination(SentenceLeaf(preprocessed_sentence, sentence_index))

    def get_last_sentence_tree(self):
        res = None
        coordinations_len = len(self.discourse_tree.coordinations)
        if coordinations_len > 0:
            res = self.discourse_tree.coordinations[len(self.discourse_tree.coordinations) - 1]

        return res

    def update(self):
        self.__process_discourse_tree_rec(self.discourse_tree)
        self.discourse_tree.clean_up()

    def __process_discourse_tree_rec(self, discourse_tree: DiscourseTree):
        if isinstance(discourse_tree, Coordination):
            for child in discourse_tree.coordinations:
                if child.is_not_processed():
                    c = child

                    if isinstance(child, Leaf):
                        new_child = self.__apply_rules(child)
                        if new_child is not None:
                            discourse_tree.replace_coordination(child, new_child)
                            c = new_child
                    child.processed = True

                    self.__process_discourse_tree_rec(c)  # recursion

        if isinstance(discourse_tree, Subordination):
            if discourse_tree.get_superordination().is_not_processed():

                if isinstance(discourse_tree.get_superordination(), Leaf):
                    new_child = self.__apply_rules(discourse_tree.get_superordination())
                    if new_child is not None:
                        discourse_tree.replace_superordination(new_child)
                    discourse_tree.get_superordination().processed = True

                    self.__process_discourse_tree_rec(discourse_tree.get_superordination())  # recursion

            if discourse_tree.get_subordination().is_not_processed():

                if isinstance(discourse_tree.get_subordination(), Leaf):
                    new_child = self.__apply_rules(discourse_tree.get_subordination())
                    if new_child is not None:
                        discourse_tree.replace_subordination(new_child)
                    discourse_tree.get_subordination().processed = True

                    self.__process_discourse_tree_rec(discourse_tree.get_subordination())  # recursion

    def __apply_rules(self, leaf: Leaf) -> DiscourseTree:
        self.logger.debug("Processing leaf:")
        self.logger.debug("")
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(str(leaf))
            self.logger.debug("")

        if not leaf.allow_split:
            self.logger.debug("Leaf will not be check.")
            return None

        self.logger.debug("Process leaf:")
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("\n" + parse_tree_visualizer.pretty_print(leaf.parse_tree))

        for rule in self.rules:
            extraction = rule.extract(leaf)
            if extraction is not None:
                self.logger.debug("Extraction rule " + rule.__class__.__name__ + " matched.")
                self.logger.debug("")
                r = extraction.generate(leaf)
                if r is not None:
                    return r
                else:
                    self.logger.debug("Reference could not be used, checking other model rules.")
                    self.logger.debug("")
        self.logger.debug("No model rule applied.")
        self.logger.debug("")

        return None
