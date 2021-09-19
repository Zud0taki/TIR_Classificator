# import necessary libraries
import cv2 as cv
import glob
import numpy as np


# define readImages
# used to read the image input with the filepath
def readImages(filepath):
    imgpath = glob.glob(r"" + filepath + "/*.tif")
    img_input = []
    for img in imgpath:
        n = cv.imread(img, -1)
        img_input.append(n)
    return img_input


# define readTxt
# used to read the txt input with the filepath
def readTxt(filepath):
    txtpath = glob.glob(r"" + filepath + "/*.txt")
    txt_input = []
    for txt in txtpath:
        txt_input.append(txt)
    return txt_input

# define checkEqualLength
# used to check if the image input and the text input are equally long
def checkEqualLength(img_input, txt_input):
    if len(img_input) == len(txt_input):
        equallength = True
    else:
        equallength = False
        #TODO Signal to TextBox - Failure
    return equallength


# define checkEqualNames
# used to check if the images and txt-files have the same names
def checkEqualNames(filepath):
    imgpath = glob.glob(r"" + filepath + "/*.tif")
    txtpath = glob.glob(r"" + filepath + "/*.txt")
    for x in range(len(imgpath)):
        imgname = str(imgpath[x])
        imgnamefirstsplit = imgname.split("\\")
        imgnametemp = imgnamefirstsplit[1]
        imgnamesecondsplit = imgnametemp.split(".tif")
        imgnamefinal = imgnamesecondsplit[0]
        txtname = str(txtpath[x])
        txtnamefirstsplit = txtname.split("\\")
        txtnametemp = txtnamefirstsplit[1]
        txtnamesecondsplit = txtnametemp.split(".txt")
        txtnamefinal = txtnamesecondsplit[0]
        if imgnamefinal == txtnamefinal:
            equalnames = True
        else:
            equalnames = False
            #TODO: Signal to Log - no accurate Names
            return equalnames
    return equalnames
