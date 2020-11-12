from enum import Enum


class Relation(Enum):
    UNKNOWN = "UNKNOWN"

    # Coordinations
    UNKNOWN_COORDINATION = "UNKNOWN_COORDINATION"  # the default for coordination
    CONTRAST = "CONTRAST"
    CAUSE_C = "CAUSE_C"
    RESULT_C = "RESULT_C"
    LIST = "LIST"
    DISJUNCTION = "DISJUNCTION"
    TEMPORAL_AFTER_C = "TEMPORAL_AFTER_C"
    TEMPORAL_BEFORE_C = "TEMPORAL_BEFORE_C"

    # Subordinations
    UNKNOWN_SUBORDINATION = "UNKNOWN_SUBORDINATION"  # the default for subordination
    ATTRIBUTION = "ATTRIBUTION"
    BACKGROUND = "BACKGROUND"
    CAUSE = "CAUSE"
    RESULT = "RESULT"
    CONDITION = "CONDITION"
    ELABORATION = "ELABORATION"
    PURPOSE = "PURPOSE"
    TEMPORAL_AFTER = "TEMPORAL_AFTER"
    TEMPORAL_BEFORE = "TEMPORAL_BEFORE"

    # for sentence simplification
    NOUN_BASED = "NOUN_BASED"
    SPATIAL = "SPATIAL"
    TEMPORAL = "TEMPORAL"
    # indicating a particular instance on a time scale (e.g. “Next Sunday 2 pm”).
    TEMPORAL_TIME = "TEMPORAL_TIME"
    # the amount of time between the two end-points of a time interval (e.g. “2 weeks").
    TEMPORAL_DURATION = "TEMPORAL_DURATION"
    # particular date (e.g. “On 7 April 2013”).
    TEMPORAL_DATE = "TEMPORAL_DATE"
    TEMPORAL_SET = "TEMPORAL_SET"
    IDENTIFYING_DEFINITION = "IDENTIFYING_DEFINITION"
    # periodic temporal sets representing times that occur with some frequency
    DESCRIBING_DEFINITION = "DESCRIBING_DEFINITION"
    # (“Every Tuesday”).
