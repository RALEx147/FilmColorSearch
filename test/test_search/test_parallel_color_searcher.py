from unittest import TestCase
from src.searcher.parallel_color_searcher import ColorSearcher
import dill
from src.kmean_cluster.cluster_utility import ClusterUtility
from src.kmean_cluster.stats.key_frame import KeyFrame


class TestColorSearcher(TestCase):
    def test_color_searcher(self):
        cluster = ClusterUtility()
        img = KeyFrame(cluster.kmeans_cluster(img='testImg.jpg', clr_num=5))
        pfile = open('pickledFrames', 'rb')
        img_data = dill.load(pfile)
        colorSearch = ColorSearcher(img)
        print(colorSearch.parallelSearch(img_data))
