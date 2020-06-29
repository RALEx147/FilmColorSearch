import cv2
import numpy as np

def crop(input):
    '''
    This method is used for crop and exclude the frame that a film may contain
    :param input: the frame to crop
    :return: a frame without black
    '''
    og = cv2.imread(input)
    img = cv2.imread(input,0)
    flag = True
    count = 0
    rows,cols = img.shape
    for i in range(cols):
        pixel = img[i, 900]
        if pixel == 0:
            count+=1
        else:
            break
    end = rows - count
    if not count > end:
        crop = og[count:end,0:img.shape[1]]
        cv2.imwrite(input[:-4] + "_crop.jpg",crop)
    else:
        print(input, "failed")

def main():
    '''
    Test method
    :return:
    '''

    file_name = "Test5.jpg"
    crop(file_name)



main()
