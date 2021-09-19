###################
# Import libraries#
###################
import cv2 as cv
import random
import matplotlib.pyplot as plt
from ConcaveHull import ConcaveHull
import glob
from Homography import *
from ShapeWriter import *
from CheckNeighborhood import *
from CheckLinearity import *


###############
# main method #
###############

def main(filepath, threshold, temperature, outputPath):
    returnlist = []
    returnlist.clear()
    imgpath = glob.glob(r"" + filepath + "/*.tif")
    img_input = []
    for img_array_counter in imgpath:
        n = cv.imread(img_array_counter, -1)
        img_input.append(n)
    txtpath = glob.glob(r"" + filepath + "/*.txt")
    txt_input = []
    for txt in txtpath:
        txt_input.append(txt)

    img_counter = len(img_input)
    txt_counter = len(txt_input)
    if img_counter == txt_counter:
        # read the images that should be checked by the algorithm
        acml_list = []
        for image_text_counter in range(len(img_input)):
            img = img_input[image_text_counter]
            with open(txt_input[image_text_counter]) as file_in:
                lines = []
                for line in file_in:
                    lines.append(line)
                linesplit = lines[1].split('\t')
                x1 = linesplit[0]
                linesplit = linesplit[1].split('\n')
                y1 = linesplit[0]
                linesplit = lines[2].split('\t')
                x2 = linesplit[0]
                linesplit = linesplit[1].split('\n')
                y2 = linesplit[0]
                linesplit = lines[3].split('\t')
                x3 = linesplit[0]
                linesplit = linesplit[1].split('\n')
                y3 = linesplit[0]
                linesplit = lines[4].split('\t')
                x4 = linesplit[0]
                linesplit = linesplit[1].split('\n')
                y4 = linesplit[0]

                # TODO Auslagern
                # create label matrix
                label_mat = np.zeros((img.shape), int)

                # find Homography
                # pts_dst = np.array([[53.27451389, 11.17915012], [53.26655878, 11.17956069], [53.26653019, 11.17806564],
                #               [53.27448475, 11.17764306]])
                pts_dst = np.array(
                    [[float(x1), float(y1)], [float(x2), float(y2)], [float(x3), float(y3)], [float(x4), float(y4)]])
                h = homographyofpicture(img, pts_dst)

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
                label_counter = 1
                checked_label_list = []
                while label_counter <= label:
                    if np.count_nonzero(label_mat == label_counter) >= 3:
                        checked_label_list.append(label_counter)
                        label_counter += 1
                    else:
                        label_counter += 1

                ####################
                # Check the pixels #
                ####################
                counter = 0
                # print(txt_input[image_text_counter])
                returnlist.append(str(txt_input[image_text_counter]))
                transformed_boundary_points = []
                # bla = checked_label_list[counter]
                while counter <= (checked_label_list.__len__() - 1):
                    for x in range(label_mat.shape[1]):
                        for y in range(label_mat.shape[0]):
                            if label_mat[y, x] == checked_label_list[counter]:
                                pts.append([y, x])

                    ###########################
                    # Concave Hull from points#
                    ###########################
                    counterbla = 0
                    # print(checked_label_list[counter])
                    returnlist.append(str(checked_label_list[counter]))
                    counterbla += 1
                    # ch = ConcaveHull()
                    # pts from above
                    # pts = [[0, 0], [1, 1], [2, 2], [3, 2]]
                    nonlinear = checkLinearity(pts)
                    # ch.loadpoints(pts)
                    if pts.__len__() > 2 and nonlinear:
                        ch = ConcaveHull()
                        ch.loadpoints(pts)
                        ch.calculatehull()
                        boundary_points = np.vstack(ch.boundary.exterior.coords.xy).T
                        transformed_boundary_points = homographypoints(h, boundary_points)
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

        with open('../Shapefile.txt', 'w') as f:
            for item in acml_list:
                f.write("%s\n" % item)
        ShapeWrite(acml_list, threshold, temperature, outputPath)

        return (returnlist)
    else:
        returnlist.append(
            "Die Anzahl der Textdateien und Bilder stimmt nicht überein. Bitte prüfen Sie den Inputordner.")
        return returnlist
