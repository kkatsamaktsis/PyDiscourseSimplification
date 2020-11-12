from __future__ import annotations

from typing import List, TextIO
import logging
import logging.config

from stanza.server import CoreNLPClient

from discoursesimplification.model.out_sentence import OutSentence
from discoursesimplification.model.simplification_content import SimplificationContent
from discoursesimplification.processing.processing_type import ProcessingType
from discoursesimplification.processing.sentence_preprocessor import SentencePreprocessor
from discoursesimplification.runner.discourse_extraction.discourse_extractor import DiscourseExtractor
from discoursesimplification.runner.discourse_tree.discourse_tree_creator import DiscourseTreeCreator
from discoursesimplification.utils.parse_tree.parse_tree_exception import ParseTreeException
from discoursesimplification.utils.sentences import sentences_utils

from discoursesimplification import config


class DiscourseSimplifier:

    def __init__(self, client: CoreNLPClient):
        self.logger = logging.getLogger(__name__)

        config.corenlp_client = client
        preprocessor = SentencePreprocessor()
        self.discourse_tree_creator = DiscourseTreeCreator(preprocessor)
        self.discourse_extractor = DiscourseExtractor()

        self.logger.debug("DiscourseSimplifier initialized")

    def do_discourse_simplification(self, sentences: List[str], proc_type: ProcessingType) -> SimplificationContent:
        if proc_type == ProcessingType.SEPARATE:
            return self.__process_separate(sentences)
        elif proc_type == ProcessingType.WHOLE:
            return self.__process_whole(sentences)
        else:
            raise ValueError("Unknown processingType.")

    def do_discourse_simplification_from_file(self, file: TextIO, proc_type: ProcessingType,
                                              separate_lines: bool = False) -> SimplificationContent:
        sentences = sentences_utils.split_into_sentences_from_file(file, separate_lines)
        return self.do_discourse_simplification(sentences, proc_type)

    def do_discourse_simplification_from_string(self, text: str, proc_type: ProcessingType) -> SimplificationContent:
        sentences = sentences_utils.split_into_sentences_from_str(text)
        return self.do_discourse_simplification(sentences, proc_type)

    def __process_whole(self, sentences: List[str]) -> SimplificationContent:
        # TODO
        pass

    # Creates a discourse tree for each individual sentence (investigates intra-sentential relations only)
    def __process_separate(self, sentences: List[str]) -> SimplificationContent:
        content = SimplificationContent()
        
        index = 0
        for sentence in sentences:
            out_sentence = OutSentence(index, sentence)

            self.logger.info("# Processing sentence {}/{} #".format(index + 1, len(sentences)))
            self.logger.info("")
            self.logger.info("'" + str(sentence) + "'")
            self.logger.info("")

            # Step 1: Create sentence discourse tree
            self.logger.debug("### Step 1) CREATE SENTENCE DISCOURSE TREE ###")
            self.logger.debug("")
            self.discourse_tree_creator.reset()
            try:
                self.discourse_tree_creator.add_sentence(sentence, index)
                self.discourse_tree_creator.update()
                if self.logger.isEnabledFor(logging.DEBUG):
                    self.logger.debug("\n" + str(self.discourse_tree_creator.discourse_tree))

                self.logger.debug("")
                self.logger.debug("### STEP 2) DO DISCOURSE EXTRACTION ###")
                elements = self.discourse_extractor.do_discourse_extraction(self.discourse_tree_creator.discourse_tree)
                for e in elements:
                    out_sentence.add_element(e)
                self.logger.debug("\n" + str(out_sentence))

            except ParseTreeException:
                self.logger.error("Failed to process sentence: " + sentence)

            content.add_sentence(out_sentence)
            index += 1

        self.logger.info("### FINISHED")
        return content
