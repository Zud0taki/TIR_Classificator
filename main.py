###################
# Import libraries#
###################
import cv2 as cv
import random
import matplotlib.pyplot as plt
from PyQt5.QtCore import QObject, pyqtSignal
from ConcaveHull import ConcaveHull
import glob
from Homography import *
from ShapeWriter import *
from CheckNeighborhood import *
from CheckLinearity import *
from InputHandler import *
from FullClassification import *


###############
# main method #
###############
class main(QObject):
    trigger = pyqtSignal()
    logstring = ""

    def run(self, filepath, threshold, temperature, outputpath):
        returnlist = []
        returnlist.clear()
        img_input = readImages(filepath)
        txt_input = readTxt(filepath)
        if checkEqualLength(img_input, txt_input):
            if checkEqualNames(filepath):
                acml_list = []
                processPicture(img_input, txt_input, threshold, returnlist, acml_list, temperature, outputpath)


        #     for x in range(len(returnlist)):
        #         self.logstring = str(returnlist[x])
        #         self.trigger.emit()
        #     return (returnlist)
        # else:
        #     returnlist.append(
        #         "Die Anzahl der Textdateien und Bilder stimmt nicht überein. Bitte prüfen Sie den Inputordner.")
        #     return returnlist
