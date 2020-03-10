from ImgKMeanObj.pic_utils import *
import PIL
import pickle
from ImgKMeanObj.stats.img_stats import *
import math
import numpy as np


def test_compare():
    picU = pic_utils
    filename = "testfile/Test2.jpg"
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
    img = []
    img.append(img_stats(colors_info))

    # create the pickle obj
    pfile = open('eximg', 'ab')

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
    img.append(img_stats(colors_info))
    pickle.dump(img, pfile)
    pfile.close()


def reshape_data_setup():
    picU = pic_utils
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


# compare the difference between two images from the most dominant color
def cal_diff(img, img1, tolerance):
    percentage = 0
    for i in range(len(img1.color_info)):
        RGB_diff = np.array(img1.color_info[i].RGB) - np.array(img.color_info[i].RGB)
        diff = math.sqrt(np.sum(RGB_diff ** 2))
        if (diff < 10 and percentage >= tolerance):
            return True
        elif diff > 10 and percentage < tolerance:
            return False
    return True


def search(filename):
    picU = pic_utils
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
    pfile = open('eximg', 'rb')
    img_data = pickle.load(pfile)
    img = img_data[0]
    img1 = img_data[1]
    print(cal_diff(img, img1))
