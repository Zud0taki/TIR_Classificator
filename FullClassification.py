# import necessary lirbraries
from CheckNeighborhood import *
import random
from CheckLinearity import *
from ConcaveHull import *
from LineSplitHomography import *
from TriplePixelCheck import *
from Export import *
from Trigger import *


# define and initialize class FullClassificator as a QObject with its variables
class FullClassificator(QObject):
    def __init__(self):
        super().__init__()
        self._img_input = ""
        self._txt_input = ""
        self._threshold1 = -1
        self._threshold2 = -1
        self._acml_list_1 = []
        self._acml_list_2 = []
        self._temp1 = -1
        self._temp2 = -1
        self._outputPath = ""
        self._numberofpolygons_1 = -1
        self._numberofpolygons_2 = -1
        self._logswitch = True
        self._img_txt_counter = 0
    progress = pyqtSignal(int)
    logstring = ""

    # define function getNumberOfPolygons
    def getNumberOfPolygons(self, list):
        counter = 0
        # hop through the given list and count up everytime it hits a seperator
        for x in range(len(list)):
            if list[x][0][0] == 0:
                counter += 1
        return counter

    # define function processPicture
    def processPicture(self):
        # hop through all images in img_input
        for image_text_counter in range(len(self._img_input)):
            self._img_txt_counter = image_text_counter
            img = self._img_input[image_text_counter]
            # open textfile to the image in img_input
            with open(self._txt_input[image_text_counter]) as file_in:
                # calculate the homography of the picture with the coordinates from the txtfile
                h = lineSplitHomography(file_in, img)

                # initiate the label_mat with an zeros/array from img_shape
                label_mat_1 = np.zeros((img.shape), int)

                # initiate the label with a zero
                label_1 = 0

                # set threshold
                threshold1 = self._threshold1

                # get image dimensions
                dimY = img.shape[0]
                dimX = img.shape[1]

                # iterate through img and check if the pixel value exceeds the threshold (if true, label pixel and call checknbh())
                for i in range(0, dimY - 1):
                    for j in range(0, dimX - 1):
                        if img[i, j] > threshold1 and label_mat_1[i, j] < 1:
                            label_1 = label_1 + 1
                            checknbh(img, label_mat_1, label_1, threshold1, j, i)

                label_img_1 = np.zeros((img.shape[0], img.shape[1], 3), float)
                labelclr_1 = np.zeros([label_mat_1.max(), 3])

                # hop through the label matrix and color each labeled pixel group random
                for i in range(label_mat_1.max() - 1):
                    labelclr_1[i, :] = [random.random(), random.random(), random.random()]

                for x in range(img.shape[1]):
                    for y in range(img.shape[0]):
                        if label_mat_1[y, x] > 0:
                            label_img_1[y, x, :] = labelclr_1[(label_mat_1[y, x] - 1), :]

                # initiate pts
                pts_1 = []

                ########################################
                # Check if a pixel label contains at least 3 pixels #
                ########################################
                checked_label_list_1 = triplePixelCheck(label_1, label_mat_1)

                ####################
                # Check the pixels #
                ####################
                counter_1 = 0
                # get image name
                imgname = str(self._txt_input[image_text_counter])
                # initiate transformed boundary points
                transformed_boundary_points_1 = []
                # fill the pts list with coordinates from the label matrix
                while counter_1 <= (checked_label_list_1.__len__() - 1):
                    for x in range(label_mat_1.shape[1]):
                        for y in range(label_mat_1.shape[0]):
                            if label_mat_1[y, x] == checked_label_list_1[counter_1]:
                                pts_1.append([y, x])

                    ############################
                    # Concave Hull from points #
                    ############################

                    # check in pts if the pixelgroups are linear
                    nonlinear_1 = checkLinearity(pts_1)
                    # proceed only if a pixelgroup has at least three members and is nonlinear
                    # condition for the creation of polygons
                    if pts_1.__len__() > 2 and nonlinear_1:
                        ch_1 = ConcaveHull()
                        ch_1.loadpoints(pts_1)
                        ch_1.calculatehull()
                        # get the exterior points of a pixel group
                        boundary_points_1 = np.vstack(ch_1.boundary.exterior.coords.xy).T
                        # use boundary points and the homography to get the transformed boundary points
                        # real world coordinates!
                        transformed_boundary_points_1 = homographypoints(h, boundary_points_1)
                        # save the transformed points in a list
                        for x in range(len(boundary_points_1)):
                            self._acml_list_1.append([boundary_points_1[x], transformed_boundary_points_1[x]])
                        # include a seperator for later use
                        self._acml_list_1.append([[0, 0], [0, 0, 0]])

                        # # Scatter for Visualization
                        # for y in pts_1:
                        #     plt.scatter(y[0], y[1], color='blue')
                        # for x in boundary_points_1:
                        #     plt.scatter(x[0], x[1], color='red')

                        # clear the points for the next cycle
                        pts_1.clear()
                        #TODO: WatchOUT for the counter - maybe needs to be deleted
                        counter_1 += 1

                        # cv2.waitKey()
                        # cv2.imshow('label_img', label_img_1)
                        # plt.show()

                    # if the condition in the beginning is not fullfilled - empty points for the next cycle
                    else:
                        pts_1.clear()
                    counter_1 += 1

                #############################################
                # Same procedure as for the first threshold #
                #############################################

                # set threshold
                threshold2 = self._threshold2

                # initiate the label_mat with an zeros/array from img_shape
                label_mat_2 = np.zeros((img.shape), int)

                # initiate the label with a zero
                label_2 = 0

                # iterate through img and check if the pixel value exceeds the threshold (if true, label pixel and call checknbh())
                for i in range(0, dimY - 1):
                    for j in range(0, dimX - 1):
                        if img[i, j] > threshold2 and label_mat_2[i, j] < 1:
                            label_2 = label_2 + 1
                            checknbh(img, label_mat_2, label_2, threshold2, j, i)

                label_img_2 = np.zeros((img.shape[0], img.shape[1], 3), float)
                labelclr_2 = np.zeros([label_mat_2.max(), 3])
                for i in range(label_mat_2.max() - 1):
                    labelclr_2[i, :] = [random.random(), random.random(), random.random()]

                for x in range(img.shape[1]):
                    for y in range(img.shape[0]):
                        if label_mat_2[y, x] > 0:
                            label_img_2[y, x, :] = labelclr_2[(label_mat_2[y, x] - 1), :]

                # initiate pts
                pts_2 = []

                ########################################
                # Check if Label has at least 3 pixels #
                ########################################
                checked_label_list_2 = triplePixelCheck(label_2, label_mat_2)


                ####################
                # Check the pixels #
                ####################
                counter = 0
                #TODO: Signal with Image Name to Status Display
                imgname = str(self._txt_input[image_text_counter])
                transformed_boundary_points = []
                while counter <= (checked_label_list_2.__len__() - 1):
                    for x in range(label_mat_2.shape[1]):
                        for y in range(label_mat_2.shape[0]):
                            if label_mat_2[y, x] == checked_label_list_2[counter]:
                                pts_2.append([y, x])

                    ###########################
                    # Concave Hull from points#
                    ###########################
                    # print(checked_label_list[counter])
                    # returnlist.append(str(checked_label_list[counter]))
                    imgname = str(self._txt_input[image_text_counter])

                    # pts from above
                    nonlinear_2 = checkLinearity(pts_2)
                    # ch.loadpoints(pts)
                    if pts_2.__len__() > 2 and nonlinear_2:
                        ch_2 = ConcaveHull()
                        ch_2.loadpoints(pts_2)
                        ch_2.calculatehull()
                        boundary_points_2 = np.vstack(ch_2.boundary.exterior.coords.xy).T
                        transformed_boundary_points_2 = homographypoints(h, boundary_points_2)
                        for x in range(len(boundary_points_2)):
                            self._acml_list_2.append([boundary_points_2[x], transformed_boundary_points_2[x]])
                        self._acml_list_2.append([[0, 0], [0, 0, 0]])

                        # Scatter for Visualization
                        # for y in pts:
                        #     plt.scatter(y[0], y[1], color='blue')
                        pts_2.clear()
                        # for x in boundary_points:
                        #     plt.scatter(x[0], x[1], color='red')

                        #TODO: Hier den Trigger oder die Klasse aufrufen!!

                    else:
                        pts_2.clear()
                    counter += 1

            # collect data from accumulated list and get the number of polygons
            # emit message to the log
            # switch logswitch
            acml_list_1 = self._acml_list_1
            nrpol = self.getNumberOfPolygons(acml_list_1)
            self._numberofpolygons_1 = nrpol
            self.progress.emit(image_text_counter)
            self._logswitch = False

            # collect data from accumulated list and get the number of polygons
            # emit message to the log
            # switch logswitch
            acml_list_2 = self._acml_list_2
            nrpol = self.getNumberOfPolygons(acml_list_2)
            self._numberofpolygons_2 = nrpol
            self.progress.emit(image_text_counter)
            self._logswitch = True


        # get the data of the accumulated list, the treshold value, the temperature value and the outputpath
        # export the results
        acml_list_1 = self._acml_list_1
        threshold1 = self._threshold1
        temp1 = self._temp1
        outputpath = self._outputPath
        export(acml_list_1, threshold1, temp1, outputpath)

        # get the data of the accumulated list, the treshold value, the temperature value and the outputpath
        # export the results
        acml_list_2 = self._acml_list_2
        threshold2 = self._threshold2
        temp2 = self._temp2
        outputpath = self._outputPath
        export(acml_list_2, threshold2, temp2, outputpath)





