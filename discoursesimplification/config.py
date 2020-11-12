

class Config:
    corenlp_client = None

    sentence_preprocessor_remove_brackets = False

    rules = [
        ["runner.discourse_tree.extraction.rules.reference_initial_conjunction_extractor",
         "ReferenceInitialConjunctionExtractor"],
        ["runner.discourse_tree.extraction.rules.reference_initial_adverbial_extractor",
         "ReferenceInitialAdverbialExtractor"],
        ["runner.discourse_tree.extraction.rules.reference_medial_adverbial_extractor",
         "ReferenceMedialAdverbialExtractor"],
        ["runner.discourse_tree.extraction.rules.reference_final_adverbial_extractor",
         "ReferenceFinalAdverbialExtractor"],
        ["runner.discourse_tree.extraction.rules.coordination_extractor", "CoordinationExtractor"],

        ["runner.discourse_tree.extraction.rules.nonrestrictive_relativeclause_whom_extractor",
         "NonRestrictiveRelativeClauseWhomExtractor"],
        ["runner.discourse_tree.extraction.rules.nonrestrictive_relativeclause_who_which_extractor",
         "NonRestrictiveRelativeClauseWhoWhichExtractor"],
        ["runner.discourse_tree.extraction.rules.nonrestrictive_relativeclause_where_extractor",
         "NonRestrictiveRelativeClauseWhereExtractor"],
        ["runner.discourse_tree.extraction.rules.nonrestrictive_relativeclause_prep_which_who_extractor",
         "NonRestrictiveRelativeClausePrepWhichWhoExtractor"],
        ["runner.discourse_tree.extraction.rules.nonrestrictive_relativeclause_whose_extractor",
         "NonRestrictiveRelativeClauseWhoseExtractor"],

        ["runner.discourse_tree.extraction.rules.restrictive_apposition_extractor", "RestrictiveAppositionExtractor"],
        ["runner.discourse_tree.extraction.rules.nonrestrictive_apposition_extractor",
         "NonRestrictiveAppositionExtractor"],

        ["runner.discourse_tree.extraction.rules.purpose_pre_extractor", "PurposePreExtractor"],
        ["runner.discourse_tree.extraction.rules.subordination_pre_purpose_extractor",
         "SubordinationPrePurposeExtractor"],
        ["runner.discourse_tree.extraction.rules.shared_np_pre_participal_extractor", "SharedNPPreParticipalExtractor"],
        ["runner.discourse_tree.extraction.rules.subordination_pre_extractor", "SubordinationPreExtractor"],

        ["runner.discourse_tree.extraction.rules.shared_np_post_coordination_extractor",
         "SharedNPPostCoordinationExtractor"],
        ["runner.discourse_tree.extraction.rules.shared_np_post_participal_extractor",
         "SharedNPPostParticipalExtractor"],
        ["runner.discourse_tree.extraction.rules.subordination_post_purpose_extractor",
         "SubordinationPostPurposeExtractor"],
        ["runner.discourse_tree.extraction.rules.purpose_post_extractor", "PurposePostExtractor"],
        ["runner.discourse_tree.extraction.rules.quoted_attribution_post_extractor", "QuotedAttributionPostExtractor"],
        ["runner.discourse_tree.extraction.rules.subordination_post_attribution_extractor2",
         "SubordinationPostAttributionExtractor2"],
        ["runner.discourse_tree.extraction.rules.subordination_post_attribution_extractor",
         "SubordinationPostAttributionExtractor"],
        ["runner.discourse_tree.extraction.rules.subordination_post_extractor", "SubordinationPostExtractor"],
        ["runner.discourse_tree.extraction.rules.quoted_attribution_pre_extractor", "QuotedAttributionPreExtractor"],
        ["runner.discourse_tree.extraction.rules.pre_attribution_extractor", "PreAttributionExtractor"],

        ["runner.discourse_tree.extraction.rules.participial_middle_extractor", "ParticipialMiddleExtractor"],

        ["runner.discourse_tree.extraction.rules.restrictive_relativeclause_who_which_extractor",
         "NonRestrictiveRelativeClauseWhoWhichExtractor"],
        ["runner.discourse_tree.extraction.rules.restrictive_relativeclause_whose_extractor",
         "RestrictiveRelativeClauseWhoseExtractor"],
        ["runner.discourse_tree.extraction.rules.restrictive_relativeclause_without_relative_pronoun_extractor",
         "RestrictiveRelativeClauseWithoutRelativePronounExtractor"],
        ["runner.discourse_tree.extraction.rules.restrictive_relativeclause_whom_extractor",
         "RestrictiveRelativeClauseWhomExtractor"],

        ["runner.discourse_tree.extraction.rules.prepositional_attachedto_vp_extractor",
         "PrepositionalAttachedtoVPExtractor"],

        ["runner.discourse_tree.extraction.rules.restrictive_participial_extractor", "RestrictiveParticipialExtractor"],

        ["runner.discourse_tree.extraction.rules.adjectival_adverbial_middle_final_extractor",
         "AdjectivalAdverbialMiddleFinalExtractor"],
        ["runner.discourse_tree.extraction.rules.adjectival_adverbial_initial_extractor",
         "AdjectivalAdverbialInitialExtractor"],

        ["runner.discourse_tree.extraction.rules.lead_np_extractor", "LeadNPExtractor"],

        ["runner.discourse_tree.extraction.rules.prepositional_initial_extractor", "PrepositionalInitialExtractor"],
        ["runner.discourse_tree.extraction.rules.prepositional_middle_final_extractor",
         "PrepositionalMiddleFinalExtractor"],

        ["runner.discourse_tree.extraction.rules.list_np.pre_list_np_extractor", "PreListNPExtractor"],
        ["runner.discourse_tree.extraction.rules.list_np.post_list_np_extractor", "PostListNPExtractor"]
    ]

    ignored_relations = [
        "UNKNOWN_COORDINATION"
    ]

    attribution_verbs = [
        "comment",
        "have faith in",
        "consider",
        "demand",
        "apprise",
        "report",
        "evince",
        "identify",
        "enlighten",
        "utter",
        "ruminate",
        "give away",
        "discern",
        "hold",
        "acknowledge",
        "explain",
        "hypothesize",
        "forbid",
        "shout",
        "theorise",
        "betray",
        "turn down",
        "traverse",
        "pipe up",
        "cogitate",
        "confide",
        "hope",
        "dispute",
        "notify",
        "conjecture",
        "televise",
        "signify",
        "read",
        "propose",
        "void",
        "express",
        "perceive",
        "mention",
        "meditate",
        "insist",
        "presume",
        "judge",
        "compute",
        "speculate",
        "discuss",
        "counter",
        "reveal",
        "contradict",
        "conceive",
        "proclaim",
        "hypothesise",
        "ascertain",
        "signal",
        "mean",
        "respond",
        "prohibit",
        "signify",
        "weight",
        "urge",
        "repudiate",
        "pronounce",
        "deduce",
        "asseverate",
        "design",
        "expect",
        "critique",
        "adjudge",
        "enounce",
        "wonder",
        "educate",
        "detect",
        "deliberate",
        "confess",
        "rehearse",
        "publish",
        "verbalize",
        "veto",
        "state",
        "suspect",
        "disprove",
        "blur",
        "manifest",
        "disclose",
        "reiterate",
        "avow",
        "slur",
        "disagree",
        "communicate",
        "enunciate",
        "disallow",
        "disclaim",
        "contemplate",
        "reason",
        "brood",
        "imagine",
        "distinguish",
        "estimate",
        "narrate",
        "surmise",
        "remark",
        "theorize",
        "clarify",
        "study",
        "disavow",
        "keep back",
        "recollect",
        "display",
        "admit",
        "credit",
        "belie",
        "entertain",
        "verbalise",
        "dismiss",
        "argue",
        "think",
        "recite",
        "invalidate",
        "abjure",
        "speak up",
        "feel",
        "relate",
        "renounce",
        "articulate",
        "assess",
        "instruct",
        "guess",
        "esteem",
        "trust",
        "teach",
        "speak",
        "ventilate",
        "guess",
        "edify",
        "acquaint",
        "connote",
        "vocalize",
        "question",
        "mediate",
        "submit",
        "mark",
        "indicate",
        "iterate",
        "whisper",
        "familiarize",
        "tell",
        "garble",
        "offer",
        "share",
        "expose",
        "regard",
        "refuse",
        "muse",
        "clue",
        "assert",
        "observe",
        "differentiate",
        "argue against",
        "recount",
        "believe",
        "count",
        "reflect on",
        "affirm",
        "recall",
        "anticipate",
        "spill",
        "controvert",
        "air",
        "warn",
        "record",
        "suppose",
        "espouse",
        "voice",
        "declare",
        "announce",
        "exhibit",
        "claim",
        "gather",
        "recognize",
        "describe",
        "influence",
        "predicate",
        "denote",
        "say",
        "deem",
        "embrace",
        "contest",
        "sense",
        "phrase",
        "allege",
        "publicise",
        "surmise",
        "ponder",
        "discriminate",
        "refute",
        "agree",
        "divulge",
        "couch",
        "note",
        "discredit",
        "reject",
        "answer",
        "oppose",
        "advise",
        "infer",
        "bear in mind",
        "repeat",
        "intend",
        "allow",
        "mispronounce",
        "reckon",
        "familiarise",
        "vocalise",
        "make known",
        "reflect",
        "concede",
        "purpose",
        "recognise",
        "recount",
        "disown",
        "broadcast",
        "deny",
        "let slip",
        "renounce",
        "remember",
        "rationalize",
        "assume",
        "bid",
        "register",
        "make out",
        "withhold",
        "inform",
        "command",
        "unburden",
        "publicize",
        "recant",
        "order",
        "talk",
        "know",
        "promote",
        "advertise",
        "swear",
        "emphasize",
        "underline",
        "testify",
        "cite",
        "message",
        "ask"
    ]

    cue_phrases = {
        "coordinating_phrases": {
            "matching": "contained",
            "phrases": {
                ("after", "TEMPORAL_AFTER_C"),
                ("although", "CONTRAST"),
                ("and", "LIST"),
                ("and after", "TEMPORAL_AFTER_C"),
                ("as", "BACKGROUND"),
                ("as a result", "RESULT_C"),
                ("as a result of", "RESULT_C"),
                ("because", "CAUSE_C"),
                ("before", "TEMPORAL_BEFORE_C"),
                ("but", "CONTRAST"),
                ("but now", "CONTRAST"),
                ("despite", "CONTRAST"),
                ("even before", "ELABORATION"),
                ("even though", "CONTRAST"),
                ("even when", "CONTRAST"),
                ("except when", "CONTRAST"),
                ("for example", "ELABORATION"),
                ("further", "ELABORATION"),
                ("however", "CONTRAST"),
                ("if", "CONDITION"),
                ("in addition", "LIST"),
                ("in addition to", "LIST"),
                ("in case", "CONDITION"),
                ("instead", "CONTRAST"),
                ("more provocatively", "ELABORATION"),
                ("moreover", "LIST"),
                ("next", "TEMPORAL_AFTER_C"),
                ("now", "BACKGROUND"),
                ("once", "BACKGROUND"),
                ("or", "DISJUNCTION"),
                ("previously", "TEMPORAL_BEFORE_C"),
                ("rather", "CONTRAST"),
                ("recently", "ELABORATION"),
                ("since", "CAUSE_C"),
                ("since(\\W(.*?\\W)?)now", "ELABORATION"),
                ("so", "ELABORATION"),
                ("so far", "ELABORATION"),
                ("still", "CONTRAST"),
                ("then", "TEMPORAL_AFTER_C"),
                ("though", "CONTRAST"),
                ("thus", "CONTRAST"),
                ("unless", "CONDITION"),
                ("until", "CONDITION"),
                ("until recently", "CONTRAST"),
                ("when", "BACKGROUND"),
                ("where", "ELABORATION"),
                ("whereby", "ELABORATION"),
                ("whether", "ELABORATION"),
                ("while", "CONTRAST"),
                ("with", "BACKGROUND"),
                ("without", "BACKGROUND"),
                ("yet", "CONTRAST")
            }
        },
        "subordinating_phrases": {
            "matching": "contained",
            "phrases": {
                ("after", "TEMPORAL_BEFORE"),
                ("although", "CONTRAST"),
                ("and", "LIST"),
                ("and after", "TEMPORAL_BEFORE"),
                ("as", "BACKGROUND"),
                ("as a result", "RESULT"),
                ("as a result of", "RESULT"),
                ("because", "CAUSE"),
                ("before", "TEMPORAL_AFTER"),
                ("but", "CONTRAST"),
                ("but now", "CONTRAST"),
                ("despite", "CONTRAST"),
                ("even before", "ELABORATION"),
                ("even though", "CONTRAST"),
                ("even when", "CONTRAST"),
                ("except when", "CONTRAST"),
                ("for example", "ELABORATION"),
                ("further", "ELABORATION"),
                ("however", "CONTRAST"),
                ("if", "CONDITION"),
                ("in addition", "LIST"),
                ("in addition to", "LIST"),
                ("in case", "CONDITION"),
                ("instead", "CONTRAST"),
                ("more provocatively", "ELABORATION"),
                ("moreover", "LIST"),
                ("next", "TEMPORAL_AFTER"),
                ("now", "BACKGROUND"),
                ("once", "BACKGROUND"),
                ("or", "DISJUNCTION"),
                ("previously", "TEMPORAL_AFTER"),
                ("rather", "CONTRAST"),
                ("recently", "ELABORATION"),
                ("since", "CAUSE"),
                ("since(\\W(.*?\\W)?)now", "ELABORATION"),
                ("so", "ELABORATION"),
                ("so far", "ELABORATION"),
                ("still", "CONTRAST"),
                ("then", "TEMPORAL_AFTER"),
                ("though", "CONTRAST"),
                ("thus", "CONTRAST"),
                ("unless", "CONDITION"),
                ("until", "CONDITION"),
                ("until recently", "CONTRAST"),
                ("when", "BACKGROUND"),
                ("where", "ELABORATION"),
                ("whereby", "ELABORATION"),
                ("whether", "ELABORATION"),
                ("while", "CONTRAST"),
                ("with", "BACKGROUND"),
                ("without", "BACKGROUND"),
                ("yet", "CONTRAST")
            }
        },
        "adverbial_phrases": {
            "matching": "exact",
            "phrases": {
                ("after", "TEMPORAL_AFTER_C"),
                ("after(\\W(.*?\\W)?)(this|that)", "TEMPORAL_AFTER_C"),
                ("although", "CONTRAST"),
                ("and", "LIST"),
                ("and after", "TEMPORAL_AFTER_C"),
                ("and after(\\W(.*?\\W)?)(this|that)", "TEMPORAL_AFTER_C"),
                ("as", "BACKGROUND"),
                ("as a result", "RESULT_C"),
                ("as a result of", "RESULT_C"),
                ("as a result of(\\W(.*?\\W)?)(this|that)", "RESULT_C"),
                ("as a result(\\W(.*?\\W)?)(this|that)", "RESULT_C"),
                ("because", "CAUSE_C"),
                ("because(\\W(.*?\\W)?)(this|that)", "CAUSE_C"),
                ("before", "TEMPORAL_BEFORE_C"),
                ("before(\\W(.*?\\W)?)(this|that)", "TEMPORAL_BEFORE_C"),
                ("but", "CONTRAST"),
                ("but now", "CONTRAST"),
                ("despite", "CONTRAST"),
                ("even before", "ELABORATION"),
                ("even though", "CONTRAST"),
                ("even when", "CONTRAST"),
                ("except when", "CONTRAST"),
                ("for example", "ELABORATION"),
                ("further", "ELABORATION"),
                ("however", "CONTRAST"),
                ("if", "CONDITION"),
                ("in addition", "LIST"),
                ("in addition to", "LIST"),
                ("in case", "CONDITION"),
                ("instead", "CONTRAST"),
                ("more provocatively", "ELABORATION"),
                ("moreover", "LIST"),
                ("next", "TEMPORAL_AFTER_C"),
                ("now", "BACKGROUND"),
                ("once", "BACKGROUND"),
                ("or", "DISJUNCTION"),
                ("previously", "TEMPORAL_BEFORE_C"),
                ("previously(\\W(.*?\\W)?)(this|that)", "TEMPORAL_BEFORE_C"),
                ("rather", "CONTRAST"),
                ("recently", "ELABORATION"),
                ("since", "CAUSE_C"),
                ("since(\\W(.*?\\W)?)now", "ELABORATION"),
                ("so", "ELABORATION"),
                ("so far", "ELABORATION"),
                ("still", "CONTRAST"),
                ("then", "TEMPORAL_AFTER_C"),
                ("though", "CONTRAST"),
                ("thus", "CONTRAST"),
                ("unless", "CONDITION"),
                ("until", "CONDITION"),
                ("until recently", "CONTRAST"),
                ("when", "BACKGROUND"),
                ("where", "ELABORATION"),
                ("whereby", "ELABORATION"),
                ("whether", "ELABORATION"),
                ("while", "CONTRAST"),
                ("with", "BACKGROUND"),
                ("without", "BACKGROUND"),
                ("yet", "CONTRAST")
            }
        },
        "default_phrases": {
            "matching": "contained",
            "phrases": {
                ("after", "TEMPORAL_AFTER_C"),
                ("although", "CONTRAST"),
                ("and", "LIST"),
                ("and after", "TEMPORAL_AFTER_C"),
                ("as", "BACKGROUND"),
                ("as a result", "RESULT_C"),
                ("as a result of", "RESULT_C"),
                ("because", "CAUSE_C"),
                ("before", "TEMPORAL_BEFORE_C"),
                ("but", "CONTRAST"),
                ("but now", "CONTRAST"),
                ("despite", "CONTRAST"),
                ("even before", "ELABORATION"),
                ("even though", "CONTRAST"),
                ("even when", "CONTRAST"),
                ("except when", "CONTRAST"),
                ("for example", "ELABORATION"),
                ("further", "ELABORATION"),
                ("however", "CONTRAST"),
                ("if", "CONDITION"),
                ("in addition", "LIST"),
                ("in addition to", "LIST"),
                ("in case", "CONDITION"),
                ("instead", "CONTRAST"),
                ("more provocatively", "ELABORATION"),
                ("moreover", "LIST"),
                ("next", "TEMPORAL_AFTER_C"),
                ("now", "BACKGROUND"),
                ("once", "BACKGROUND"),
                ("or", "DISJUNCTION"),
                ("previously", "TEMPORAL_BEFORE_C"),
                ("rather", "CONTRAST"),
                ("recently", "ELABORATION"),
                ("since", "CAUSE_C"),
                ("since(\\W(.*?\\W)?)now", "ELABORATION"),
                ("so", "ELABORATION"),
                ("so far", "ELABORATION"),
                ("still", "CONTRAST"),
                ("then", "TEMPORAL_AFTER_C"),
                ("though", "CONTRAST"),
                ("thus", "CONTRAST"),
                ("unless", "CONDITION"),
                ("until", "CONDITION"),
                ("until recently", "CONTRAST"),
                ("when", "BACKGROUND"),
                ("where", "ELABORATION"),
                ("whereby", "ELABORATION"),
                ("whether", "ELABORATION"),
                ("while", "CONTRAST"),
                ("with", "BACKGROUND"),
                ("without", "BACKGROUND"),
                ("yet", "CONTRAST")
            }
        }
    }