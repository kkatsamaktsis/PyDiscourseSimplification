from __future__ import annotations

from typing import List
import logging.config

from discoursesimplification.utils.parse_tree.parse_tree_parser import ParseTreeParser
from discoursesimplification.utils.sentences import sentences_utils
from nltk import Tree
from stanza.server import CoreNLPClient

from discoursesimplification.processing.discourse_simplifier import DiscourseSimplifier
from discoursesimplification.processing.processing_type import ProcessingType


logging.config.fileConfig('logging.conf', defaults={'logfilename': './ouput.log', 'logfilemode': 'w'})
logger = logging.getLogger('ROOT')


def save_lines(file, lines: List[str]):
    pass


def parse_tree_to_str(parse_tree: Tree):
    return str(parse_tree).replace("\\s+", " ").replace("[\\n\\t]", "")\
                .replace("\n", "").replace("\t", "")


def save_parse_trees(input_file_name: str):
    parse_trees_as_str = ""
    input_file_obj = open(input_file_name + '.txt')
    sentences = sentences_utils.split_into_sentences_from_file(input_file_obj, True)

    i = 0
    for sentence in sentences:
        parse_trees_as_str += (parse_tree_to_str(ParseTreeParser.parse(sentence)) + "\n")
        print(i)
        i += 1

    with open(input_file_name + '_file_parse_trees.txt', 'w') as output_file:
        output_file.write(parse_trees_as_str)


file_name = "input"
input_file = open(file_name + '.txt')
ENGLISH_CUSTOM_PROPS = {"typedDependenciesCollapsed": True, "retainTmpSubcategories": True}

with CoreNLPClient(
        annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'parse', 'depparse', 'coref'],
        timeout=30000,
        memory='6G',
        properties=ENGLISH_CUSTOM_PROPS,
        be_quiet=True) as client:
        
    discourse_simplifier = DiscourseSimplifier(client)
    content = discourse_simplifier.do_discourse_simplification_from_file(input_file, ProcessingType.SEPARATE, True)

    with open(file_name + '_file_output.json', 'w') as out_file:
        out_file.write(content.serialize_to_json())

    with open(file_name + '_file_output_default.txt', 'w') as out_file:
        out_file.write(content.default_format(False))

    with open(file_name + '_file_output_flat.txt', 'w') as out_file:
        out_file.write(content.flat_format(False))

    with open(file_name + '_file_simplified.txt', 'w') as out_file:
        out_file.write(content.get_simplified_sentences_as_simple_text())

    save_parse_trees("input")

    logger.info("")
    logger.info("done")
