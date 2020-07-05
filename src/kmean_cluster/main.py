from src.kmean_cluster.cluster_utility import ClusterUtility
from PIL import Image
import pickle
from src.kmean_cluster.stats.key_frame import *
from src.kmean_cluster.color_match import cal_diff


def test_compare():
    # Initialize ClusterUtility
    picU = ClusterUtility

    # default filename
    filename = "../../test/test_cluster_utility/testfile/Test2.jpg"

    # If you want to create a smaller size of for a better test speed
    # Uncomment the following
    i1 = Image.open(filename)
    i1 = i1.resize((100, 100), Image.ANTIALIAS)
    filename = filename[:4] + "_reshape.jpg"
    i1.save(filename)
    out_name_2 = filename[:-4] + "_out.jpg"

    colors_info = picU.kmeans_cluster(filename, 5, False)
    # picU.img_color_compare("testfile/Test95_out.jpg","testfile/Test99_out.jpg")

    # grab the stats data of the image and create the image obj local
    img = []
    img.append(KeyFrame(colors_info))

    # create the pickle obj
    pfile = open('testing_pickle.pickle', 'ab')

    filename = "../../test/test_cluster_utility/testfile/Test4.jpg"
    # out_name_1 = filename[:-4] + "_out.jpg"
    # picU.kmeans_cluster(filename, 5, True, out_name_1)
    i1 = Image.open(filename)
    i1 = i1.resize((100, 100), Image.ANTIALIAS)
    filename = filename[:4] + "_reshape.jpg"
    i1.save(filename)
    out_name_2 = filename[:-4] + "_out.jpg"
    colors_info = picU.kmeans_cluster(filename, 5, False, out_name_2)
    # picU.img_color_compare("testfile/Test95_out.jpg","testfile/Test99_out.jpg")

    # grab the stats data of the image and create the image obj local
    img.append(KeyFrame(colors_info))
    pickle.dump(img, pfile)
    pfile.close()


def pickle_img_data_sample():
    '''
    This method is a sample method for create a database of pickled object for all frames of movie.
    In this sample, we take one picture as an example. For the future modification, we need to change the filename
    to the directory where we have our film frames, and loop the kmeans_cluster function. It is likely we can optimize
    the speed with the multi-thread. This method will run for each film in our database and should run on server.
    :return: None
    '''

    # Initialize ClusterUtility
    picU = ClusterUtility

    # default filename
    filename = "../../test/test_cluster_utility/testfile/Test2.jpg"

    # Calculate the color info
    colors_info = picU.kmeans_cluster(filename, 5, False)
    # picU.img_color_compare("testfile/Test95_out.jpg","testfile/Test99_out.jpg")

    # grab the stats data of the image and create the image obj local
    img = []
    img.append(KeyFrame(colors_info))

    # create the pickle obj
    pfile = open('testing_pickle.pickle', 'ab')
    pickle.dump(img, pfile)
    pfile.close()

def reshape_data_setup():
    picU = ClusterUtility
    a = 1
    b = 125
    for i in range(a, b):
        filename = "testfile/Test" + str(i) + ".jpg"
        i1 = Image.open(filename)
        i1 = i1.resize((100, 100), Image.ANTIALIAS)
        filename = "testfile-out/Test" + str(i) + "_reshape.jpg"
        i1.save(filename)
    print("FINISHED RESHAPE")
    for j in range(a, b):
        filename = "testfile-out/Test" + str(j) + "_reshape.jpg"
        out2 = filename[:-4] + "_out.jpg"
        picU.kmeans_cluster(filename, 10, True, out2)

def search(filename):
    '''
    This method is a TEST method, should be replaced by the parallel_color_searcher
    :param filename:
    :return:
    '''
    picU = ClusterUtility
    picU.kmeans_cluster(filename, 10, True, "cache/temp.jpg")
    a = 1
    b = 125
    fbar = "cache/temp.jpg"
    print("Finished read data")
    count = 0
    for i in range(a, b):
        cur_data = "testfile-out/Test" + str(i) + "_reshape_out.jpg"
        diff = picU.img_color_compare(fbar, cur_data)

        if (diff < 1) and (count < 7):
            i1 = Image.open("testfile/Test" + str(i) + ".jpg")
            i1.show()
            print("Difference (percentage):", diff)
            # count += 1;
        print("Next")


if __name__ == "__main__":
    test_compare()  # initialize the database
    pfile = open('testing_pickle.pickle', 'rb')
    img_data = pickle.load(pfile)
    img = img_data[0]
    img1 = img_data[1]
    print(cal_diff(img, img1))
