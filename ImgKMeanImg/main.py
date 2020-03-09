from ImgKMeanImg.pic_utils import *


def test_compare():
    picU = pic_utils
    filename = "testfile/Test95.jpg"
    out_name_1 = filename[:-4] + "_out.jpg"
    picU.kmeans_cluster(filename, 5, True, out_name_1)
    i1 = Image.open(filename)
    i1 = i1.resize((100, 100), PIL.Image.ANTIALIAS)
    filename = filename[:4] + "_reshape.jpg"
    i1.save(filename)
    out_name_2 = filename[:-4] + "_out.jpg"
    picU.kmeans_cluster(filename, 5, True, out_name_2)
    picU.img_color_compare("testfile/Test95_out.jpg", "testfile/Test99_out.jpg")


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
    search("testfile-out/Test2_reshape.jpg")
