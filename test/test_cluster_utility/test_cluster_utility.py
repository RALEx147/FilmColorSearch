from unittest import TestCase
import os
from src.kmean_cluster.cluster_utility import ClusterUtility
import dill
from src.kmean_cluster.stats.key_frame import KeyFrame
import pathos.multiprocessing as mp
class TestClusterUtility(TestCase):


    def getListOfFiles(self,dirName):
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

    def test_cluster(self):
        '''
        Test k-means cluster and pickled method into KeyFrame objects and load the pickle data from file
        :return: None
        '''
        listOfFiles = self.getListOfFiles('./testfile')
        cluster = ClusterUtility
        TestLen = 10
        img = []
        for i in range(TestLen):
            colors_info = cluster.kmeans_cluster(listOfFiles[i],5,False)
            img.append(KeyFrame(colors_info))

        # create the pickle obj
        # if the pickled file exists, remove the file and create a new
        if os.path.exists('pickledFrames.pickle'):
            os.remove('pickledFrames.pickle')
        pfile = open('pickledFrames.pickle', 'ab')
        dill.dump(img, pfile)
        pfile.close()
        pfile = open('pickledFrames.pickle', 'rb')
        img_data = dill.load(pfile)
        TestCase.assertEqual(TestLen,len(img_data))

    def test_multiprocess_cluster(self):
        '''
        Using multiprocess, test k-means cluster and pickled method into KeyFrame objects and load the pickle data from file.
        :return: None
        '''
        listOfFiles = self.getListOfFiles('./testfile')
        cluster = ClusterUtility
        TestLen = 10
        img = []
        p = mp.Pool(2)

        for i in range(TestLen):
            colors_info = cluster.kmeans_cluster(listOfFiles[i], 5, False)
            img.append(KeyFrame(colors_info))

        # create the pickle obj
        # if the pickled file exists, remove the file and create a new
        if os.path.exists('pickledFrames.pickle'):
            os.remove('pickledFrames.pickle')
        pfile = open('pickledFrames.pickle', 'ab')
        dill.dump(img, pfile)
        pfile.close()
        pfile = open('pickledFrames.pickle', 'rb')
        img_data = dill.load(pfile)
        TestCase.assertEqual(TestLen, len(img_data))