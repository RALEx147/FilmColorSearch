__author__ = "Jacky Lin"
__date__ = "June 17, 2020$"

import numpy as np
from multiprocessing import Pool
from ..kmean_cluster.color_match import *
from ..kmean_cluster.stats import *
class ColorSearcher:
    def __init__(self, ctl_frame, sorting):
        # the controlling frame
        self.ctl_frame = ctl_frame
        # store boolean telling us if we should sort the results
        self.sorting = sorting

    # CALL paralleSearch INSTEAD OF THIS
    def search(self, other_frame):
        '''
        This method calculated the color difference of the controlling frame with a series of given other frames
        :param other_frame: a series of frames to compare
        :return: a series of score.
        '''

        # initialize the dictionary of results
        results = {}

        # loop over the index
        results[other_frame]=cal_diff(self.ctl_frame.color_dist,other_frame.color_dist)

        # return the results
        return results

    # CALL THIS INSTEAD OF SEARCH
    def parallelSearch(self, other_frames, n=8):

        # TODO: try different values of n above and compare run time, optimize n.
        # note: this should be done on the server machine, as the optimal n value
        # will be system dependent.

        # could also try parallelizing just the search, or just the sort, neither, or both...& compare runtime

        # create a pool of n processes to parallelize the search and sort across
        # (n=8, to test. try different n values and compare runtime)
        p = Pool(n);
        # map the search function across the queryFeatures in parallel
        results = p.map(self.search, other_frames)
        # if the above line causes an error, try
        # results = p.map(self.search, (queryFeatures,))
#TODO-modify the following code
        # parallelized sort
        # sort the results, so that the more relevant results
        # (smaller numbers) are at the front of the list
        if self.sorting == True:
            # map the sorting function across the processes of the pool
            results = p.map(sorted,[(v, k) for (k, v) in results.items()])
            # if the above line causes an error, try
            # results = p.map(sorted,([(v,k) for (k,v) in results.items()],))

        # return the results
        return results