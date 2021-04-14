from typing import List
from discoursesimplification import config


def lemmatize(word: str):
    ann = config.corenlp_client.annotate(word, annotators=['tokenize', 'ssplit', 'lemma'])
    sentence = ann.sentence[0]
    for token in sentence.token:
        return token.lemma


def words_to_string(words: List[any]):
    return ' '.join(words)


def capitalize_word(word):
    if len(word) > 0:
        word = word[0].upper() + word[1:]

    return word


def lowercase_word(word):
    return word.lower()


def words_to_proper_sentence(words: List[any]):
    res = []
    res.extend(words)

    for c in [".", ","]:
        prev = None
        i = 0
        while i < len(res):
            word = res[i]

            if word == c:
                if prev is None or prev == word:
                    del res[i]
                    i -= 1
            prev = word
            i += 1

        if len(res) > 0 and res[len(res) - 1] == c:
            del res[len(res) - 1]

    # add a '.' at the end
    res.append(".")

    # capitalize first word
    if len(res) > 0:
        res[0] = capitalize_word(res[0])

    return res


def words_to_proper_sentence_string(words: List[any]):
    return words_to_string(words_to_proper_sentence(words))
