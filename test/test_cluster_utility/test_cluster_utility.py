from unittest import TestCase
import os
from src.kmean_cluster.cluster_utility import ClusterUtility
import dill
from src.kmean_cluster.stats.key_frame import KeyFrame
import pathos.multiprocessing as mp
import time
from _thread import start_new_thread
import threading


class TestClusterUtility(TestCase):

    def getListOfFiles(self, dirName):
        '''
        For the given path, get the List of all files in the directory tree
        :param dirName: directory
        :return: a list of file names
        '''
        # create a list of file and sub directories
        # names in the given directory
        listOfFile = os.listdir(dirName)
        allFiles = list()
        # Iterate over all the entries
        for entry in listOfFile:
            # Create full path
            fullPath = os.path.join(dirName, entry)
            # If entry is a directory then get the list of files in this directory
            if os.path.isdir(fullPath):
                allFiles = allFiles + self.getListOfFiles(fullPath)
            else:
                allFiles.append(fullPath)

        return allFiles

    def cluster(self, num_of_files):
        '''
        Test k-means cluster and pickled method into KeyFrame objects and load the pickle data from file
        :return: None
        '''
        start_time = time.time()
        list_of_files = self.getListOfFiles('./testfile')
        cluster = ClusterUtility
        test_len = num_of_files
        img = []
        for i in range(test_len):
            colors_info = cluster.kmeans_cluster(list_of_files[i], 5)
            img.append(KeyFrame(colors_info))
        cluster_time = time.time() - start_time
        # create the pickle obj
        # if the pickled file exists, remove the file and create a new
        if os.path.exists('../test_search/pickledFrames'):
            os.remove('../test_search/pickledFrames')
        pfile = open('../test_search/pickledFrames', 'ab')
        dill.dump(img, pfile)
        pfile.close()
        pfile = open('../test_search/pickledFrames', 'rb')
        img_data = dill.load(pfile)
        t = TestCase()
        t.assertEqual(test_len, len(img_data))
        return cluster_time

    def multiprocess_cluster(self, number_of_files, number_of_process):
        '''
        Using multiprocess, test k-means cluster and pickled method into KeyFrame objects and load the pickle data from file.
        :return: None
        '''
        start_time = time.time()

        # define a nested function for multiprocessing
        def cluster_f(file):
            colors_info = cluster.kmeans_cluster(file, 5)
            return KeyFrame(colors_info)

        # get the directory of all files
        list_of_files = self.getListOfFiles('./testfile')
        # use 10 file for test
        test_len = number_of_files
        # initialize cluster utility
        cluster = ClusterUtility
        # using 5 process
        p = mp.Pool(number_of_process)
        # multiprocessing
        # store a list of KeyFrames
        img = p.map(cluster_f, list_of_files[:test_len])
        p.close()
        p.join()
        cluster_time = time.time() - start_time
        # create the pickle obj
        # if the pickled file exists, remove the file and create a new
        if os.path.exists('../test_search/pickledFrames'):
            os.remove('../test_search/pickledFrames')
        pfile = open('../test_search/pickledFrames', 'ab')
        dill.dump(img, pfile)
        pfile.close()
        pfile = open('../test_search/pickledFrames', 'rb')
        img_data = dill.load(pfile)
        test_case = TestCase()
        pfile.close()
        test_case.assertEqual(test_len, len(img_data))
        return cluster_time

    def multithread_cluster(self, num_of_files, num_of_threads):
        '''
        Using multithread, test k-means cluster and pickled method into KeyFrame objects and load the pickle data from file.
        :rtype: int
        :return: None
        '''
        start_time = time.time()

        # define a nested function for multiprocessing
        def cluster_f(files, result, index):
            for j in range(len(files)):
                colors_info = cluster.kmeans_cluster(files[j], 5)
                result[index+j] = KeyFrame(colors_info)

        # get the directory of all files
        list_of_files = self.getListOfFiles('./testfile')
        # initialize cluster utility
        cluster = ClusterUtility
        # create a list of threads
        threads = [None] * num_of_threads
        # a list of result to store files
        results = [None] * num_of_files
        # calculate the number of jobs needs to assign to each thread
        num_of_jobs_for_each = int(num_of_files / num_of_threads)
        # the number of remaining jobs to assign
        remain_jobs = int(num_of_files % num_of_threads)

        for i in range(num_of_threads):
            # assign n jobs as we calculated above to each thread
            tasks = list_of_files[i * num_of_jobs_for_each : (i+1) * num_of_jobs_for_each]
            # add additional jobs to thread
            if remain_jobs > 0:
                remain_jobs -= 1
                tasks += [list_of_files[-1*remain_jobs]]
            # assign task to thread
            threads[i] = threading.Thread(target=cluster_f, args=(tasks, results, i))
            # start the thread
            threads[i].start()
        # do some other stuff
        for i in range(len(threads)):
            threads[i].join()

        cluster_time = time.time() - start_time
        # create the pickle obj
        # if the pickled file exists, remove the file and create a new
        if os.path.exists('../test_search/pickledFrames'):
            os.remove('../test_search/pickledFrames')
        file = open('../test_search/pickledFrames', 'ab')
        dill.dump(results, file)
        file.close()
        file = open('../test_search/pickledFrames', 'rb')
        img_data = dill.load(file)
        test_case = TestCase()
        test_case.assertEqual(num_of_files, len(img_data))
        file.close()
        return cluster_time

    def test_cluster_time(self):
        num_of_files = 30
        num_of_thread = 8
        # time = self.cluster(num_of_files)
        # time = self.multiprocess_cluster(num_of_files, num_of_thread)
        time = self.multithread_cluster(num_of_files, num_of_thread)
        print(time)