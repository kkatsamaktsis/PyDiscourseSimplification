from discoursesimplification.runner.discourse_tree.relation import Relation

"""
    UNKNOWN_COORDINATION.coordination = true;
    CONTRAST.coordination = true;
    CAUSE_C.coordination = true;
    RESULT_C.coordination = true;
    LIST.coordination = true;
    DISJUNCTION.coordination = true;
    TEMPORAL_AFTER_C.coordination = true;
    TEMPORAL_BEFORE_C.coordination = true;
        
    CAUSE.coordinate_version = CAUSE_C
    RESULT.coordinate_version = RESULT_C
    TEMPORAL_AFTER.coordinate_version = TEMPORAL_AFTER_C
    TEMPORAL_BEFORE.coordinate_version = TEMPORAL_BEFORE_C

    CAUSE_C.subordinate_version = CAUSE
    RESULT_C.subordinate_version = RESULT
    TEMPORAL_AFTER_C.subordinate_version = TEMPORAL_AFTER
    TEMPORAL_BEFORE_C.subordinate_version = TEMPORAL_BEFORE

    CAUSE_C.inverse = RESULT_C
    RESULT_C.inverse = CAUSE_C
    TEMPORAL_AFTER_C.inverse = TEMPORAL_BEFORE_C
    TEMPORAL_BEFORE_C.inverse = TEMPORAL_AFTER_C
    CAUSE.inverse = RESULT
    RESULT.inverse = CAUSE
    TEMPORAL_AFTER.inverse = TEMPORAL_BEFORE
    TEMPORAL_BEFORE.inverse = TEMPORAL_AFTER
"""


def is_coordination(relation: Relation):
    return relation == Relation.UNKNOWN_COORDINATION \
           or relation == Relation.CONTRAST \
           or relation == Relation.CAUSE_C \
           or relation == Relation.RESULT_C \
           or relation == Relation.LIST \
           or relation == Relation.DISJUNCTION \
           or relation == Relation.TEMPORAL_AFTER_C \
           or relation == Relation.TEMPORAL_BEFORE_C


def get_coordinate_version(relation: Relation):
    res_dict = {
        relation.CAUSE: relation.CAUSE_C,
        relation.RESULT.coordinate_version: relation.RESULT_C,
        relation.TEMPORAL_AFTER.coordinate_version: relation.TEMPORAL_AFTER_C,
        relation.TEMPORAL_BEFORE.coordinate_version: relation.TEMPORAL_BEFORE_C
    }

    if relation in res_dict:
        return res_dict[relation]
    else:
        return None


def get_subordinate_version(relation: Relation):
    res_dict = {
        relation.CAUSE_C: relation.CAUSE,
        relation.RESULT_C: relation.RESULT,
        relation.TEMPORAL_AFTER_C: relation.TEMPORAL_AFTER,
        relation.TEMPORAL_BEFORE_C:  relation.TEMPORAL_BEFORE
    }

    if relation in res_dict:
        return res_dict[relation]
    else:
        return None


# This is only used in coordinations
def get_inverse(relation: Relation):
    res_dict = {
        relation.CAUSE_C: relation.RESULT_C,
        relation.RESULT_C: relation.CAUSE_C,
        relation.TEMPORAL_AFTER_C: relation.TEMPORAL_BEFORE_C,
        relation.TEMPORAL_BEFORE_C: relation.TEMPORAL_AFTER_C,
        relation.CAUSE: relation.RESULT,
        relation.RESULT: relation.CAUSE,
        relation.TEMPORAL_AFTER: relation.TEMPORAL_BEFORE,
        relation.TEMPORAL_BEFORE: relation. TEMPORAL_AFTER,
    }

    if relation in res_dict:
        return res_dict[relation]
    else:
        return relation


def str_to_relation(relation_str: str):
    return Relation[relation_str]
