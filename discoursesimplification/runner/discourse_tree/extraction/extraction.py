from typing import List

from discoursesimplification.runner.discourse_tree.relation import Relation
from discoursesimplification.runner.discourse_tree import relation_utility
from discoursesimplification.runner.discourse_tree.model.coordination import Coordination
from discoursesimplification.runner.discourse_tree.model.discourse_tree import DiscourseTree
from discoursesimplification.runner.discourse_tree.model.leaf import Leaf
from discoursesimplification.runner.discourse_tree.model.subordination import Subordination
from discoursesimplification.utils.words import words_utils


class Extraction:
    def __init__(self, extraction_rule: str, referring: bool, cue_phrase_words: List[any], relation: Relation,
                 context_right: bool, constituents: List[Leaf]):
        if referring and len(constituents) != 1:
            raise AssertionError("Referring relations should have one constituent")

        if not referring and not relation_utility.is_coordination(relation) and len(constituents) != 2:
            raise AssertionError("(Non-referring) subordinate relations rules should have two constituents")

        self.extraction_rule = extraction_rule
        self.referring = referring
        self.cue_phrase = None if cue_phrase_words is None else words_utils.words_to_string(cue_phrase_words)
        self.relation = relation
        self.context_right = context_right
        self.constituents = constituents

    def generate(self, curr_child: Leaf) -> DiscourseTree:
        if relation_utility.is_coordination(self.relation):
            if self.referring:
                # find previous node to use as a reference
                prev_node = curr_child.get_previous_node()
                if prev_node is not None and prev_node.usable_as_reference():
                    # use prev node as a reference
                    prev_node.use_as_reference()

                    res = Coordination(self.extraction_rule, self.relation, self.cue_phrase, [])
                    res.add_coordination(prev_node)  # set prev node as a reference
                    res.add_coordination(self.constituents[0])

                    return res
            else:
                return Coordination(self.extraction_rule, self.relation, self.cue_phrase, list(self.constituents))
        else:
            if self.referring:
                # find previous node to use as a reference
                prev_node = curr_child.get_previous_node()
                if prev_node is not None and prev_node.usable_as_reference():
                    # use prev node as a reference
                    prev_node.use_as_reference()

                    res = Subordination(self.extraction_rule, self.relation, self.cue_phrase, Leaf(),  # temp
                                        self.constituents[0], self.context_right)
                    res.replace_left_constituent(prev_node)  # set prev node as a reference

                    return res
            else:
                return Subordination(self.extraction_rule, self.relation, self.cue_phrase, self.constituents[0],
                                     self.constituents[1], self.context_right)

        return None
