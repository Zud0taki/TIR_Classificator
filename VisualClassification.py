# import necessary libraries and methods
import cv2 as cv
import random
from CheckNeighborhood import *
from CheckLinearity import *

# define visualclassification
# used to threshold a picture and manipulate found pixels
def visualclassification(img_input, threshold1, threshold2, outputpath):
    for x in range(len(img_input)):
        img = img_input[x]

        label = 0
        label_mat = np.zeros((img.shape), int)

        # get image dimensions
        dimY = img.shape[0]
        dimX = img.shape[1]
        # iterate through img and check if the pixel value exceeds the threshold (if true, label pixel and call checknbh())
        for i in range(0, dimY - 1):
            for j in range(0, dimX - 1):
                if img[i, j] > threshold1 and label_mat[i, j] < 1:
                    label = label + 1
                    checknbh(img, label_mat, label, threshold1, j, i)

        label_img = np.zeros((img.shape[0], img.shape[1], 3), float)
        output_img = np.zeros((img.shape[0], img.shape[1]), int)
        labelclr = np.zeros([label_mat.max(), 3])
        for i in range(label_mat.max() - 1):
            labelclr[i, :] = [random.random(), random.random(), random.random()]

        for x in range(img.shape[1]):
            for y in range(img.shape[0]):
                if label_mat[y, x] > 0:
                    label_img[y, x, :] = labelclr[(label_mat[y, x] - 1), :]
                    img[y, x] = 63000

        output_1_mani = "manipulated original" + outputpath + "/" + str(x) + str(threshold1) + "dn.tif"
        output_1_colored = "colored result" + outputpath + "/" + str(x) + str(threshold1) + "dn.tif"
        cv.imshow("color_img", label_img)
        cv.imshow("manipulated original", img)
        # cv.imwrite(output_1_mani, img)
        # cv.imwrite(output_1_colored, label_img)
