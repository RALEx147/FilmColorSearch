import cv2
import numpy as np
import math


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
        weighted_diff += diff * cmp_img.color_dist[i].percent
    return weighted_diff

def cal_diff_treshold(ctr_img, cmp_img, threshold=100):
    """
    The function to compare the difference between two images from the most dominant color
    The calculation is based on the Delta CIE76.
    The formula for individual color difference is diff = sqrt((R1-R2)^2+(G1-G2)^2+(B1-B2)^2)
    We add the percentage contains in the certain color to generate the weighted difference.
    Given that the color information for each image is on descending order based on the dominance
    of the color, we calculate the most significant color first.
    :param threshold: the percentage of color difference to compare, it should be a number from 0 to 100 and
    the default value is 100
    :param ctr_img: The control group of the image, it is usually the image user upload
    :param cmp_img: The image to compare with the control group.
    :return: weighted_diff: a float weighted number based on the difference between two image
    """
    threshold = threshold / 100
    weighted_diff = 0
    calculated_percent = 0
    for i in range(len(cmp_img.color_info)):
        # calculate the difference of the color distribution
        RGB_diff = np.array(cmp_img.color_info[i].RGB) - np.array(ctr_img.color_info[i].RGB)
        diff = math.sqrt(np.sum(RGB_diff ** 2))
        calculated_percent += cmp_img.color_info[i].percent
        if calculated_percent >= threshold:
            break
        print(diff, cmp_img.color_info[i].percent)
        weighted_diff += diff * cmp_img.color_info[i].percent
    return weighted_diff
