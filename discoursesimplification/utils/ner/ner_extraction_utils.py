from __future__ import annotations

from discoursesimplification.utils.index_range import IndexRange
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from discoursesimplification.utils.ner.ner_string import NERString

NO_CATEGORY = "O"


def get_ner_index_ranges(ner_string: NERString):
    res = []

    for group in ner_string.groups:
        res.append(IndexRange(group.get_from_token_index(), group.get_to_token_index()))

    return res
