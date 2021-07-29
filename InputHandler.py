import cv2 as cv
import glob
import numpy as np


def readImages(filepath):
    imgpath = glob.glob(r"" + filepath + "/*.tif")
    img_input = []
    for img_array_counter in imgpath:
        n = cv.imread(img_array_counter, -1)
        img_input.append(n)
    return img_input


def readTxt(filepath):
    txtpath = glob.glob(r"" + filepath + "/*.txt")
    txt_input = []
    for txt in txtpath:
        txt_input.append(txt)
    return txt_input


def checkEqualLength(img_input, txt_input):
    if len(img_input) == len(txt_input):
        equallength = True
    else:
        equallength = False
        #TODO Signal to TextBox - Failure
    return equallength


