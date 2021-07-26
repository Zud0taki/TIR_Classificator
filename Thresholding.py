import cv2
import numpy as np

import cv2 as cv
import random
import matplotlib.pyplot as plt
from ConcaveHull import ConcaveHull
import glob
from Homography import *
from ShapeWriter import *
from CheckNeighborhood import *
from CheckLinearity import *
from PIL import Image


def thresholding():
    filePath = r"C:\Users\DLR_OS_Testbench\Desktop\DummyOrdner"
    threshold = 18600
    imgpath = glob.glob(r"" + filePath + "/*.tif")
    img_input = []
    for img_array_counter in imgpath:
        n = cv.imread(img_array_counter, -1)
        img_input.append(n)

    for x in range(len(img_input)):
        img = img_input[x]

        th = threshold
        label = 0
        label_mat = np.zeros((img.shape), int)

        # get image dimensions
        dimY = img.shape[0]
        dimX = img.shape[1]

        # iterate through img and check if the pixel value exceeds the threshold (if true, label pixel and call checknbh())
        for i in range(0, dimY - 1):
            for j in range(0, dimX - 1):
                if img[i, j] > th and label_mat[i, j] < 1:
                    label = label + 1
                    checknbh(img, label_mat, label, th, j, i)

        label_img = np.zeros((img.shape[0], img.shape[1], 3), float)
        output_img = np.zeros((img.shape[0], img.shape[1]), int)
        labelclr = np.zeros([label_mat.max(), 3])
        for i in range(label_mat.max() - 1):
            labelclr[i, :] = [random.random(), random.random(), random.random()]

        for x in range(img.shape[1]):
            for y in range(img.shape[0]):
                if label_mat[y, x] > 0:
                    label_img[y, x, :] = labelclr[(label_mat[y, x] - 1), :]

        for x in range(img.shape[1]):
            for y in range(img.shape[0]):
                if label_mat[y, x] > 0:
                    output_img[y, x] = label_mat[y, x]

        imageinput = Image.fromarray(img)
        imagematrix = Image.fromarray(label_img)
        yeet = imageinput.paste(imagematrix, (0, 0), imagematrix)

        yeet.save('test', "PNG")

        # dst = cv2.addWeighted(label_img, 0.5, img, 0.7, 0)
        cv2.imshow('sas', yeet)
        cv2.waitKey(0)

        cv.imshow("img", label_img)
        cv.waitKey()


solution = thresholding()
