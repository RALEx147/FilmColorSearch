import cv2

def crop(input_img, output_img = None):
    '''
    This method is used for crop and exclude masked film images
    :param input_img: the image to crop
    :param output_img: the file_name for output image, default value is the name of input image + "_out.jpg"
    :return: a image without black mask
    '''
    og = cv2.imread(input_img)
    img = cv2.imread(input_img, 0)
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
        if output_img == None:
            output_img = input_img[:-4] + "_crop.jpg"
        cv2.imwrite(output_img, crop)
    else:
        print(input_img, "failed")

