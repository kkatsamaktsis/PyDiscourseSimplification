# PyDiscourseSimplification

A translation in python 3.7 of [Discourse Simplification](https://github.com/Lambda-3/DiscourseSimplification), the core component of the [Graphene](https://github.com/Lambda-3/Graphene) project.

A python project for simplifying sentences and transforming them to discourse/rhetorical structures.

## Dependencies
  - [python3.7](https://www.python.org/)
  - [stanza](https://github.com/stanfordnlp/stanza)
  - [nltk](https://www.nltk.org/)

    For development [PyCharm Community](https://www.jetbrains.com/pycharm/) is recommended

## Setup

    python3.7 setup.py sdist
    pip3.7 install ./dist/discoursesimplification-0.0.1.tar.gz


### Run the program
Create a new text file with the input

    nano input.txt
     
Run program

    python3.7 app.py
    
Inspect output

    cat input_file_output_default.txt
    cat input_file_output_flat.txt
    cat input_file_output.json
    cat input_file_simplified.txt
    cat input_file_parse_trees.txt

## Use as library
Check `app.py`. 
    
## Use from Python interpreter

    $ python3.7 setup.py sdist
    $ pip3.7 install ./dist/discoursesimplification-0.0.1.tar.gz
    $ python3.7
    Python 3.7.6 (v3.7.6:43364a7ae0, Dec 18 2019, 14:18:50)
    [Clang 6.0 (clang-600.0.57)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>>
    >>> from stanza.server import CoreNLPClient
    >>> client = CoreNLPClient(annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'parse', 'depparse', 'coref'], timeout=30000, memory='6G', be_quiet=True)
    >>>
    >>> from discoursesimplification.processing.discourse_simplifier import DiscourseSimplifier
    >>> from discoursesimplification.processing.processing_type import ProcessingType
    >>>
    >>> discourse_simplifier = DiscourseSimplifier(client)
    >>> content = discourse_simplifier.do_discourse_simplification_from_string("We will walk, although it rains", ProcessingType.SEPARATE)
    >>>
    >>> print(content.default_format(False))
    
    # We will walk, although it rains

    3633bf7b62b344348dbf0114e8661294        0       We will walk .
            L:CONTRAST      3193cd29e24145599c87ca408448ba4d

    3193cd29e24145599c87ca408448ba4d        0       It rains .
            L:CONTRAST      3633bf7b62b344348dbf0114e8661294

    >>> print(content.get_simplified_sentences_as_simple_text())
    We will walk . It rains . 

    >>>
    >>> client.stop()
    >>> exit()
 
## Author
Konstantinos Katsamaktsis
