from discoursesimplification.runner.discourse_tree.extraction.rules.list_np.list_np_extractor import ListNPExtractor


class PostListNPExtractor(ListNPExtractor):
    def __init__(self):
        super().__init__("ROOT <<: (S < (NP $.. (VP << (NP=np))))")
