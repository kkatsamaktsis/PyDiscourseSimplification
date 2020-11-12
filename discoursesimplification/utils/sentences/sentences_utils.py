from typing import List, TextIO
import io


def split_into_sentences_from_stringio(buff: io.StringIO) -> List[str]:
    res = []

    while True:
        sentence = buff.readline().strip()
        if sentence == '':
            break
        res.append(sentence)

    return res


def split_into_sentences_from_str(text: str) -> List[str]:
    return split_into_sentences_from_stringio(io.StringIO(text))


def split_into_sentences_from_file(file: TextIO, by_lines: bool) -> List[str]:
    # file_content = file.read()
    if by_lines:
        res = []

        while True:
            line = file.readline()
            if not line:
                break
            res.append(line.strip())

        file.close()

        return res
    else:
        # TODO
        raise Exception("Implement: splitIntoSentences(new BufferedReader(new FileReader(file)));")
