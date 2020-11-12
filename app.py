from __future__ import annotations

from typing import List
import logging.config

from stanza.server import CoreNLPClient

from discoursesimplification.processing.discourse_simplifier import DiscourseSimplifier
from discoursesimplification.processing.processing_type import ProcessingType


logging.config.fileConfig('logging.conf', defaults={'logfilename': './ouput.log', 'logfilemode': 'w'})
logger = logging.getLogger('ROOT')


def save_lines(file, lines: List[str]):
    pass


input_file = open('input.txt')

with CoreNLPClient(
        annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'parse', 'depparse', 'coref'],
        timeout=30000,
        memory='16G',
        be_quiet=True) as client:
        
    discourse_simplifier = DiscourseSimplifier(client)
    content = discourse_simplifier.do_discourse_simplification_from_file(input_file, ProcessingType.SEPARATE, True)

    with open('output.json', 'w') as out_file:
        out_file.write(content.serialize_to_json())

    with open('output_default.txt', 'w') as out_file:
        out_file.write(content.default_format(False))

    with open('output_flat.txt', 'w') as out_file:
        out_file.write(content.flat_format(False))

    logger.info("")
    logger.info("done")
