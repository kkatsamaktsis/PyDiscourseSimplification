from discoursesimplification.utils.parse_tree.parse_tree_exception import ParseTreeException
from discoursesimplification import config
from nltk.tree import Tree

from discoursesimplification.utils.word import Word


class ParseTreeParser:

    @staticmethod
    def convert_parse_tree_to_nltk_tree(parse_tree) -> Tree:
        return Tree(Word(parse_tree.value),
                    [ParseTreeParser.convert_parse_tree_to_nltk_tree(child) for child in
                     parse_tree.child]) if parse_tree.child else Word(parse_tree.value)

    @staticmethod
    def print_tree(parse_tree) -> None:
        ParseTreeParser.convert_parse_tree_to_nltk_tree(parse_tree).pretty_print()

    @staticmethod
    def parse(text: str) -> Tree:
        # Parse wih stanza default pipeline
        # nlp = stanza.Pipeline(lang='en', processors='tokenize, lemma, pos, depparse', logging_level='INFO')
        # doc = nlp(text)
        # raw_words = doc.sentences[0].tokens
        # print(raw_words)
        # best_parse = doc.sentences[0].tokens

        # Parse with NLP client:
        ann = config.corenlp_client.annotate(text, annotators=['tokenize', 'ssplit', 'parse', 'depparse'])

        # get the constituency parse of the first sentence
        sentence = ann.sentence[0]
        # constituency_parse = sentence.binarizedParseTree
        constituency_parse = sentence.parseTree
        best_parse = constituency_parse

        if best_parse is None:
            raise ParseTreeException(text)

        # Convert to nltk Tree to be able to access instance methods
        return ParseTreeParser.convert_parse_tree_to_nltk_tree(best_parse)
