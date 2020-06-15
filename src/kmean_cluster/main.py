from cluster_utility import *
import PIL
import pickle
from stats.key_frame import *
import math
import numpy as np


def test_compare():
    picU = ClusterUtility
    filename = "testfile/Test2.jpg"
    # out_name_1 = filename[:-4] + "_out.jpg"
    # picU.kmeans_cluster(filename, 5, True, out_name_1)
    i1 = Image.open(filename)
    # Create a smaller size of for a better test speed
    i1 = i1.resize((100, 100), PIL.Image.ANTIALIAS)
    filename = filename[:4] + "_reshape.jpg"
    i1.save(filename)
    out_name_2 = filename[:-4] + "_out.jpg"
    colors_info = picU.kmeans_cluster(filename, 5, False, out_name_2)
    # picU.img_color_compare("testfile/Test95_out.jpg","testfile/Test99_out.jpg")

    # grab the stats data of the image and create the image obj local
    img = []
    img.append(KeyFrame(colors_info))

    # create the pickle obj
    pfile = open('testing_pickle.pickle', 'ab')

    filename = "testfile/Test4.jpg"
    # out_name_1 = filename[:-4] + "_out.jpg"
    # picU.kmeans_cluster(filename, 5, True, out_name_1)
    i1 = Image.open(filename)
    i1 = i1.resize((100, 100), PIL.Image.ANTIALIAS)
    filename = filename[:4] + "_reshape.jpg"
    i1.save(filename)
    out_name_2 = filename[:-4] + "_out.jpg"
    colors_info = picU.kmeans_cluster(filename, 5, False, out_name_2)
    # picU.img_color_compare("testfile/Test95_out.jpg","testfile/Test99_out.jpg")

    # grab the stats data of the image and create the image obj local
    img.append(KeyFrame(colors_info))
    pickle.dump(img, pfile)
    pfile.close()


def reshape_data_setup():
    picU = ClusterUtility
    a = 1
    b = 125
    for i in range(a, b):
        filename = "testfile/Test" + str(i) + ".jpg"
        i1 = Image.open(filename)
        i1 = i1.resize((100, 100), PIL.Image.ANTIALIAS)
        filename = "testfile-out/Test" + str(i) + "_reshape.jpg"
        i1.save(filename)
    print("FINISHED RESHAPE")
    for j in range(a, b):
        filename = "testfile-out/Test" + str(j) + "_reshape.jpg"
        out2 = filename[:-4] + "_out.jpg"
        picU.kmeans_cluster(filename, 10, True, out2)


def cal_diff(ctr_img, cmp_img):
    """
    The function to compare the difference between two images from the most dominant color
    The calculation is based on the Delta CIE76.
    The formula for individual color difference is diff = sqrt((R1-R2)^2+(G1-G2)^2+(B1-B2)^2)
    We add the percentage contains in the certain color to generate the weighted difference.
    Given that the color information for each image is on descending order based on the dominance
    of the color, we calculate the most significant color first.
    :param ctr_img: The control group of the image, it is usually the image user upload
    :param cmp_img: The image to compare with the control group.
    :return: weighted_diff: a float weighted number based on the difference between two image
    """
    weighted_diff = 0
    for i in range(len(cmp_img.color_dist)):
        # calculate the difference of the color distribution
        RGB_diff = np.array(cmp_img.color_dist[i].RGB) - np.array(ctr_img.color_dist[i].RGB)
        diff = math.sqrt(np.sum(RGB_diff ** 2))
        print(diff, cmp_img.color_dist[i].percent)
        weighted_diff += diff * cmp_img.color_dist[i].percent
    return weighted_diff


def search(filename):
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
