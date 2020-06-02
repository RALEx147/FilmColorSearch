'''
To cluster the image through K-mean using the OpenCV package
url = "https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/"
'''
# import the necessary packages
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import cv2
from PIL import Image
from .stats.ColorInfo import Color_info


class pic_utils:

    def kmeans_cluster(img, clr_num, save=False, save_name="out.jpg"):
        # load the image and convert it from BGR to RGB so that
        # we can dispaly it with matplotlib
        image = cv2.imread(img)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # show our image
        plt.figure()
        # plt.axis("off")
        plt.imshow(image)

        # reshape the image to be a list of pixels
        image = image.reshape((image.shape[0] * image.shape[1], 3))
        clt = KMeans(n_clusters=clr_num)
        clt.fit(image)
        # build a histogram of clusters and then create a figure
        # representing the number of pixels labeled to each color
        hist = pic_utils.centroid_histogram(clt)
        bar, colors_info = pic_utils.plot_colors(hist, clt.cluster_centers_)
        # show our color bart
        res = plt.figure()
        plt.axis("off")
        plt.imshow(bar)
        # plt.show()
        # save the file
        if (save):
            res.savefig(save_name)
        plt.close('all')
        return colors_info

    def centroid_histogram(clt):
        # grab the number of different clusters and create a histogram
        # based on the number of pixels assigned to each cluster
        num_labels = np.arange(0, len(np.unique(clt.labels_)) + 1)
        (hist, _) = np.histogram(clt.labels_, bins=num_labels)
        # normalize the histogram, such that it sums to one
        hist = hist.astype("float")
        hist /= hist.sum()
        # return the histogram
        return hist

    def plot_colors(hist, centroids):
        # initialize the bar chart representing the relative frequency
        # of each of the colors
        bar = np.zeros((50, 300, 3), dtype="uint8")
        startX = 0
        # collection for the colors and their dominance percentage
        colors_info = []
        # loop over the percentage of each cluster and the color of
        # each cluster
        for (percent, color) in zip(hist, centroids):
            # plot the relative percentage of each cluster
            endX = startX + (percent * 300)
            cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                          color.astype("uint8").tolist(), -1)
            startX = endX
            # store each individual data info the color info
            temp = Color_info(percent * 100, color)
            colors_info.append(temp)
        # return the bar chart
        return bar, colors_info

    def img_color_compare(i1_dic, i2_dic):
        i1 = Image.open(i1_dic)
        i2 = Image.open(i2_dic)
        # i1 = i1.resize((100, 100), PIL.Image.ANTIALIAS)
        # i2 = i2.resize((100, 100), PIL.Image.ANTIALIAS)
        assert i1.mode == i2.mode, "Different kinds of images."
        assert i1.size == i2.size, "Different sizes."

        pairs = zip(i1.getdata(), i2.getdata())
        if len(i1.getbands()) == 1:
            # for gray-scale jpegs
            dif = sum(abs(p1 - p2) for p1, p2 in pairs)
        else:
            dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

        ncomponents = i1.size[0] * i1.size[1] * 3
        # print("Difference (percentage):", (dif / 255.0 * 100) / ncomponents)

        return (dif / 255.0 * 100) / ncomponents
