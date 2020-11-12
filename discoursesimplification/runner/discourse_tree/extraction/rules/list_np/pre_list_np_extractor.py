from discoursesimplification.runner.discourse_tree.extraction.rules.list_np.list_np_extractor import ListNPExtractor


class PreListNPExtractor(ListNPExtractor):
    def __init__(self):
        super().__init__("ROOT <<: (S < (NP=np $.. VP))")
