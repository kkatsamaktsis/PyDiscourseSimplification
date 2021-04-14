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
    
   
## Author
Konstantinos Katsamaktsis
