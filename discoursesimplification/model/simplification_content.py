from __future__ import annotations

import json

from nltk import Tree

from discoursesimplification.model.element import Element
from discoursesimplification.model.simple_context import SimpleContext
from discoursesimplification.runner.discourse_tree.relation import Relation

# if TYPE_CHECKING:
from discoursesimplification.model.out_sentence import OutSentence


def parse_tree_to_str(parse_tree: Tree):
    return str(parse_tree).replace("\\s+", " ").replace("[\\n\\t]", "")\
                .replace("\n", "").replace("\t", "")


def get_simplification_content_with_tree_as_str(content: SimplificationContent) -> SimplificationContent:
    new_content = SimplificationContent()
    for sentence in content.sentences:
        new_element_dict = {}
        for key in sentence.element_dict.keys():
            element = sentence.element_dict[key]
            parse_tree_str = parse_tree_to_str(element.parse_tree)
            new_element_dict[key] = Element(element.parse_tree, element.sentence_index, element.context_layer)
            new_element_dict[key].parse_tree = parse_tree_str  # set to str for json representation
            new_element_dict[key].id = element.id
            for simple_context in element.simple_contexts:
                new_simple_context = SimpleContext(simple_context.parse_tree)
                new_simple_context.relation = simple_context.relation
                new_simple_context.parse_tree = parse_tree_to_str(simple_context.parse_tree)
                new_element_dict[key].add_simple_context(new_simple_context)
            for linked_context in element.linked_contexts:
                new_element_dict[key].add_linked_context(linked_context)

        new_sentence = OutSentence(sentence.sentence_index, sentence.original_sentence)
        new_sentence.element_dict = new_element_dict
        new_content.add_sentence(new_sentence)
    return new_content


class ContentEncoder(json.JSONEncoder):
    def default(self, o):
        # Primitive types
        if isinstance(o, int):
            return o
        if isinstance(o, bool):
            return o
        if isinstance(o, str):
            return o
        # No need for float

        # enum type
        if isinstance(o, Relation):
            return o.value

        if isinstance(o, SimpleContext):
            r = dict(o.__dict__)
            if "phrase" in r.keys():
                del r["phrase"]
            return dict(r)

        # custom object types
        if isinstance(o, dict):
            return o

        return o.__dict__


class SimplificationContent:

    def __init__(self):
        self.sentences = []

    def add_sentence(self, sentence: OutSentence):
        self.sentences.append(sentence)

    def add_element(self, element: Element):
        self.sentences[element.sentence_index].add_element(element)

    def get_element(self, input_id: str):
        for sentence in self.sentences:
            e = sentence.get_element(input_id)
            if e is not None:
                return e
        
        return None

    def default_format(self, resolve: bool) -> str:
        res = ""

        for out_sentence in self.sentences:
            res += ("\n# " + out_sentence.original_sentence + "\n")
            for element in out_sentence.get_elements():
                res += ("\n" + element.id + "\t" + str(element.context_layer) + "\t" + element.text + "\n")
                for simple_context in element.simple_contexts:
                    res += ("\t" + "S:" + str(simple_context.relation.value) + "\t" + simple_context.text + "\n")
                for linked_context in element.linked_contexts:
                    if resolve:
                        res += ("\t" + "L:" + str(linked_context.relation.value) + "\t"
                                + self.get_element(linked_context.target_id).text + "\n")
                    else:
                        res += ("\t" + "L:" + str(linked_context.relation.value) + "\t"
                                + linked_context.target_id + "\n")
        
        return res

    def flat_format(self, resolve: bool) -> str:
        res = ""

        for out_sentence in self.sentences:
            for element in out_sentence.get_elements():
                res += (out_sentence.original_sentence + "\t" + element.id + "\t" + str(element.context_layer) + "\t"
                        + element.text)
                for simple_context in element.simple_contexts:
                    res += ("\t" + "S:" + str(simple_context.relation.value) + "(" + simple_context.text + ")")
                for linked_context in element.linked_contexts:
                    if resolve:
                        res += ("\t" + "L:" + str(linked_context.relation.value) + "("
                                + self.get_element(linked_context.target_id).text + ")")
                    else:
                        res += ("\t" + "L:" + str(linked_context.relation.value) + "("
                                + linked_context.target_id + ")")

        return res

    def serialize_to_json(self) -> str:
        return json.dumps(get_simplification_content_with_tree_as_str(self), cls=ContentEncoder)

    def get_simplified_sentences_as_simple_text(self) -> str:
        res = ""

        for out_sentence in self.sentences:
            for element in out_sentence.get_elements():
                res += (element.text + " ")
                for simple_context in element.simple_contexts:
                    res += (simple_context.text + " ")
                # for linked_context in self.linked_contexts:
                #     res += ("\t" + "L:" + str(linked_context.relation) + "(" + linked_context.target_id + ")");
            res += "\n"

        return res

    def __str__(self):
        return "\n".join(list(map(lambda s: str(s), self.sentences)))
