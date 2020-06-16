__author__ = "Dale Hartman"
__date__ = "July 21, 2016 3:38:40 PM$"

import numpy as np
from multiprocessing import Pool

class ColorSearcher:
    def __init__(self, index, sorting):
        # store the index we are reading through
        self.index = index
        # store boolean telling us if we should sort the results
        self.sorting = sorting

    # CALL paralleSearch INSTEAD OF THIS
    def search(self, queryFeatures):
        """
        Take the descriptor of our search image and compute
        the best matching images from the index
        """

        # initialize the dictionary of results
        results = {}

        # loop over the index
        for (k, features) in self.index.items():
            # compute the chi-squared distance between the features
            # in our index and our query features
            d = self.chi2_distance(features, queryFeatures)

            # now update the results dictionary with that result
            results[k] = d

        # return the results
        return results

    # CALL THIS INSTEAD OF SEARCH
    def parallelSearch(self, queryFeatures, n=8):

        # TODO: try different values of n above and compare run time, optimize n.
        # note: this should be done on the server machine, as the optimal n value
        # will be system dependent.

        # could also try parallelizing just the search, or just the sort, neither, or both...& compare runtime

        # create a pool of n processes to parallelize the search and sort across
        # (n=8, to test. try different n values and compare runtime)
        p = Pool(n);
        # map the search function across the queryFeatures in parallel
        results = p.map(self.search, queryFeatures)
        # if the above line causes an error, try
        # results = p.map(self.search, (queryFeatures,))

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

    def chi2_distance(self, histA, histB, eps = 1e-10):
        # compute the chi-squared distance
        d = 0.5 * np.sum([((a-b) ** 2) / (a + b + eps)
            for (a, b) in zip(histA, histB)])

        # return the chi-squared distance
        return d