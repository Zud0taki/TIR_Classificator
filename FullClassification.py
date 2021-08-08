from PyQt5.QtCore import QObject, pyqtSignal

from CheckNeighborhood import *
import random
from CheckLinearity import *
from ConcaveHull import *
import matplotlib.pyplot as plt
from LineSplitHomography import *
from TriplePixelCheck import *
from Export import *

class Classificator(QObject):
    trigger = pyqtSignal()
    logstring=""


def processPicture(img_input, txt_input, threshold, returnlist, acml_list, temperature, outputpath):
    for image_text_counter in range(len(img_input)):
        img = img_input[image_text_counter]
        with open(txt_input[image_text_counter]) as file_in:
            h = lineSplitHomography(file_in, img)

            # initiate the label_mat with an zeros/array from img_shape
            label_mat = np.zeros((img.shape), int)

            # initiate the label with a zero
            label = 0

            # set threshold
            th = threshold

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
            labelclr = np.zeros([label_mat.max(), 3])
            for i in range(label_mat.max() - 1):
                labelclr[i, :] = [random.random(), random.random(), random.random()]

            for x in range(img.shape[1]):
                for y in range(img.shape[0]):
                    if label_mat[y, x] > 0:
                        label_img[y, x, :] = labelclr[(label_mat[y, x] - 1), :]

            # initiate pts
            pts = []

            ########################################
            # Check if Label has at least 3 pixels #
            ########################################
            checked_label_list = triplePixelCheck(label, label_mat)


            ####################
            # Check the pixels #
            ####################
            counter = 0
            #TODO: Signal with Image Name to Status Display
            imgname = str(txt_input[image_text_counter])
            Classificator.logstring = "Bild: " + imgname
            #Classificator.trigger.emit()
            returnlist.append(str(txt_input[image_text_counter]))
            transformed_boundary_points = []
            while counter <= (checked_label_list.__len__() - 1):
                for x in range(label_mat.shape[1]):
                    for y in range(label_mat.shape[0]):
                        if label_mat[y, x] == checked_label_list[counter]:
                            pts.append([y, x])

                ###########################
                # Concave Hull from points#
                ###########################
                # print(checked_label_list[counter])
                returnlist.append(str(checked_label_list[counter]))
                imgname = str(txt_input[image_text_counter])
                Classificator.logstring = "Bild: " + imgname

                # pts from above
                nonlinear = checkLinearity(pts)
                # ch.loadpoints(pts)
                if pts.__len__() > 2 and nonlinear:
                    ch = ConcaveHull()
                    ch.loadpoints(pts)
                    ch.calculatehull()
                    boundary_points = np.vstack(ch.boundary.exterior.coords.xy).T
                    transformed_boundary_points = HomographyPoints(h, boundary_points)
                    for x in range(len(boundary_points)):
                        acml_list.append([boundary_points[x], transformed_boundary_points[x]])
                    acml_list.append([[0, 0], [0, 0, 0]])
                    for y in pts:
                        plt.scatter(y[0], y[1], color='blue')
                    pts.clear()
                    for x in boundary_points:
                        plt.scatter(x[0], x[1], color='red')
                    # cv.waitKey()
                    # cv.imshow('label_img', label_img)
                    # plt.show()
                    # boundary_points is a subset of pts corresponding to the concave hull
                else:
                    # print("Das Label musste übersprungen werden, da es nicht genug Pixel gab, um das Polygon zu aufzuspannen.")
                    returnlist.append(
                        "Das Label musste übersprungen werden, da es nicht genug Pixel gab, um das Polygon zu aufzuspannen.")
                    pts.clear()
                counter += 1

        #insert here Export
    export(acml_list, threshold, temperature, outputpath)
        # for x in range(len(returnlist)):
        #     self.logstring = str(returnlist[x])
        #     self.trigger.emit()


