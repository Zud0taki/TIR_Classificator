# import necessary libraries and functions
import sys
from PyQt5.QtCore import QThread
from main import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from CameraModes import *
from FullClassification import FullClassificator
from InputHandler import *
from VisualClassification import *


# MainWindow is the Class of the Graphical User Interface
# define the class as QDialog and initialize it with its variables
class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        loadUi("Classificator.ui", self)
        self._browse_files_btn.clicked.connect(self.browseinput)
        self._browse_output_btn.clicked.connect(self.browseoutput)
        self._start_btn.clicked.connect(self.startclassification)
        self._threshold_slider.sliderMoved.connect(self.getslidervalue)
        self._threshold_slider_2.sliderMoved.connect(self.getslidervalue)
        self._profile1_radio.toggled.connect(lambda: self.checkradiostate(self._profile1_radio))
        self._profile2_radio.toggled.connect(lambda: self.checkradiostate(self._profile2_radio))
        self._profile3_radio.toggled.connect(lambda: self.checkradiostate(self._profile3_radio))
        self._classificationb_selection_combox.currentIndexChanged.connect(self.getcombovalue)
        self._numberOfPoints = ""

        self.statepolygons1 = 0
        self.statepolygons2 = 0

    # define getcombovalue
    # used to get the value from the combobox in the GUI
    def getcombovalue(self):
        ComboValue = self._classificationb_selection_combox.currentIndex()
        # print(ComboValue)
        return ComboValue

    # define loggingdisplay
    # used to display a message in the status_display
    def loggingdisplay(self, message):
        self._status_display.append(message)

    # define checkforthresh
    # used to check for the radio button position - camera profile
    def checkforcameramode(self):
        camera_pointer = 0
        if self._profile1_radio.isChecked():
            camera_pointer = 1
            return camera_pointer
        if self._profile2_radio.isChecked():
            camera_pointer = 2
            return camera_pointer
        if self._profile3_radio.isChecked():
            camera_pointer = 3
            return camera_pointer

    # define checkradiostate
    # used to adjust displayed information based on the position of the radiobutton
    def checkradiostate(self, radio):
        if radio.text() == "Mode 1: - 40°C bis 120°C":
            if radio.isChecked():
                self._threshold_slider.setMinimum(-41)
                self._threshold_slider.setMaximum(121)
                self._threshold_slider.setTickInterval(10)
                self._threshold_slider_2.setMinimum(-41)
                self._threshold_slider_2.setMaximum(121)
                self._threshold_slider_2.setTickInterval(10)
                self._lowerbound_label.setText("-40°C")
                self._upperbound_label.setText("120°C")
                print("Mode 1 selected")

        if radio.text() == "Mode 2:     0°C bis 500°C":
            if radio.isChecked():
                self._threshold_slider.setMinimum(-1)
                self._threshold_slider.setMaximum(501)
                self._threshold_slider.setTickInterval(100)
                self._threshold_slider_2.setMinimum(-1)
                self._threshold_slider_2.setMaximum(501)
                self._threshold_slider_2.setTickInterval(100)
                self._lowerbound_label.setText("0°C")
                self._upperbound_label.setText("500°C")
                print("Mode 2 selected")

        if radio.text() == "Mode 3: 300°C bis 1200°C":
            if radio.isChecked():
                self._threshold_slider.setMinimum(299)
                self._threshold_slider.setMaximum(1201)
                self._threshold_slider.setTickInterval(100)
                self._threshold_slider_2.setMinimum(299)
                self._threshold_slider_2.setMaximum(1201)
                self._threshold_slider_2.setTickInterval(100)
                self._lowerbound_label.setText("300°C")
                self._upperbound_label.setText("1200°C")
                print("Mode 3 selected")

    # define getslidervalue
    # used to get the temperature slider values
    def getslidervalue(self):
        threshold = self._threshold_slider.value()
        th = str(threshold)
        self._thresholdv_label.setText(th)
        threshold2 = self._threshold_slider_2.value()
        th2 = str(threshold2)
        self._thresholdv_label_2.setText(th2)
        thresholds = [threshold, threshold2]
        return thresholds

    # define getpaths
    # used to read the given input- and outputpath
    def getpaths(self):
        imgpath = r"" + self._filename_input.text()
        outputPath = r"" + self._output_input.text()
        pathlist = [imgpath, outputPath]
        return pathlist

    # define browseoutput
    # used to open an explorer for the output-folder selection
    def browseoutput(self):
        outputpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Output Folder')
        self._output_input.setText(outputpath)

    # define browseinput
    # used to open an explorer for the output-folder selection
    def browseinput(self):
        imgpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Image Folder')
        self._filename_input.setText(imgpath)

    # define printoutput
    # used to gather information of the GUI, given by the user
    # depending on logswitch variable - log for first or second threshold
    def printoutput(self):
        logswitch = self.worker._logswitch
        img_input = self.worker._img_input
        img_txt_counter = self.worker._img_txt_counter
        pathlist = self.getpaths()
        filePath = pathlist[0]
        imgpath = glob.glob(r"" + filePath + "/*.tif")
        imgname = str(imgpath[img_txt_counter])
        imgnamefirstsplit = imgname.split("\\")
        imgnamelistlength = len(imgnamefirstsplit)
        imgnametemp = imgnamefirstsplit[imgnamelistlength - 1]
        imgnamesecondsplit = imgnametemp.split(".tif")
        imgnamefinal = imgnamesecondsplit[0]

        if logswitch:
            allpolygons1 = self.worker._numberofpolygons_1
            statepolygons1 = self.statepolygons1
            displaypolygons1 = allpolygons1 - statepolygons1
            self.statepolygons1 = allpolygons1
            self._numberOfPoints_1 = str(self.worker._numberofpolygons_1)
            self._browse_status.append(
                "In Bild " + imgnamefinal + " wurden neue Polygone (TH1) gefunden. Anzahl: " + str(
                    displaypolygons1) + ". Für Threshold 1 bekannte Polygone: " + self._numberOfPoints_1)
        elif logswitch == False:
            allpolygons2 = self.worker._numberofpolygons_2
            statepolygons2 = self.statepolygons2
            displaypolygons2 = allpolygons2 - statepolygons2
            self.statepolygons2 = allpolygons2
            self._numberOfPoints_2 = str(self.worker._numberofpolygons_2)
            self._browse_status.append(
                "In Bild " + imgnamefinal + " wurden neue Polygone (TH2) gefunden. Anzahl: " + str(
                    displaypolygons2) + ". Für Threshold 2 bekannte Polygone: " + self._numberOfPoints_2)

    # define createthread
    # used to create a thread for the main program to run in, while logging visually for the user
    def createthread(self, img_input, txt_input, threshold1, threshold2, acml_list_1, acml_list_2, temp1, temp2,
                     outputPath):
        # set up thread and worker
        self.thread = QThread()
        self.worker = FullClassificator()
        # set up the variables
        self.worker._img_input = img_input
        self.worker._txt_input = txt_input
        self.worker._threshold1 = threshold1
        self.worker._threshold2 = threshold2
        self.worker._acml_list_1 = acml_list_1
        self.worker._acml_list_2 = acml_list_2
        self.worker._temp1 = temp1
        self.worker._temp2 = temp2
        self.worker._outputPath = outputPath
        # move the worker to the thread
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.processPicture)
        self.worker.progress.connect(self.printoutput)
        # start the thread
        self.thread.start()

    # define startclassification
    # used to start the programme
    def startclassification(self):
        # set up status messages
        status1 = "Status des Klassifikators: Running"
        status2 = "Status des Klassifikators: Beendet"
        status3 = "Fehler: Nicht die gleiche Anzahl an .tif und .txt Dateien gefunden"
        status4 = "Fehler: Nicht die gleichen Namen für .tif und .txt Dateien gefunden"

        # get the combobox value - depending on that respond set the working profile of the classificator
        # TODO: switch between profiles
        # set the status bar to running
        self._status_field.append(status1)
        # get paths and split the list into input and outputpath
        pathlist = self.getpaths()
        filePath = pathlist[0]
        outputPath = pathlist[1]
        comboValue = self.getcombovalue()
        # check radiostate and set the treshold_pointer
        threshold_pointer = self.checkforcameramode()
        if threshold_pointer == 0:
            self._browse_status.append("Es wurde kein Kameramodus gewählt.")
        elif threshold_pointer == 1:

            # get the temperature values from the sliders and convert to strings for display
            temperatures = self.getslidervalue()
            temp1 = temperatures[0]
            temp1str = str(temp1)
            temp2 = temperatures[1]
            temp2str = str(temp2)
            # convert the temperature values to threshold 16-Bit values
            threshold1 = firstmode(temp1)
            threshold1str = str(threshold1)
            threshold2 = firstmode(temp2)
            threshold2str = str(threshold2)
            # append log window
            self._browse_status.append(
                "Der erste Threshold wurde auf " + threshold1str + "°C (" + threshold1str + " dn) gesetzt")
            self._browse_status.append(
                "Der zweite Threshold wurde auf " + threshold2str + "°C (" + threshold2str + " dn) gesetzt")
            self._browse_status.append("Klassifikation wird gestartet.")
            # get img_input and txt_input
            img_input = readImages(filePath)
            txt_input = readTxt(filePath)
            # check if img_input and txt_input have the same amount of members
            if checkEqualLength(img_input, txt_input):
                # if true - check if the names of the files are identical
                if checkEqualNames(filePath):
                    # if true - start classification
                    acml_list_1 = []
                    acml_list_2 = []
                    self.createthread(img_input, txt_input, threshold1, threshold2, acml_list_1, acml_list_2, temp1,
                                      temp2, outputPath)
                else:
                    # if false - stop
                    self._status_field.append(status4)
            else:
                # if false- stop
                self._status_field.append(status3)
            # after finishing classification - append status to signal finish to user
            self._status_field.append(status2)

        elif threshold_pointer == 2:

            # get the temperature values from the sliders and convert to strings for display
            temperatures = self.getslidervalue()
            temp1 = temperatures[0]
            temp1str = str(temp1)
            temp2 = temperatures[1]
            temp2str = str(temp2)
            # convert the temperature values to threshold 16-Bit values
            threshold1 = secondmode(temp1)
            threshold1str = str(threshold1)
            threshold2 = secondmode(temp2)
            threshold2str = str(threshold2)
            # append log window
            self._browse_status.append(
                "Der erste Threshold wurde auf " + threshold1str + "°C (" + threshold1str + " dn) gesetzt")
            self._browse_status.append(
                "Der zweite Threshold wurde auf " + threshold2str + "°C (" + threshold2str + " dn) gesetzt")
            self._browse_status.append("Klassifikation wird gestartet.")
            # get img_input and txt_input
            img_input = readImages(filePath)
            txt_input = readTxt(filePath)
            if comboValue == 0:
                print("Full Classification")
                # check if img_input and txt_input have the same amount of members
                if checkEqualLength(img_input, txt_input):
                    # if true - check if the names of the files are identical
                    if checkEqualNames(filePath):
                        # if true - start classification
                        acml_list_1 = []
                        acml_list_2 = []
                        self.createthread(img_input, txt_input, threshold1, threshold2, acml_list_1, acml_list_2, temp1,
                                          temp2, outputPath)
                    else:
                        # if false - stop
                        self._status_field.append(status4)
                else:
                    # if false- stop
                    self._status_field.append(status3)

            elif comboValue == 1:
                print("Visual Classification")
                visualclassification(img_input, threshold1, threshold2, outputPath)


            # after finishing classification - append status to signal finish to user
            self._status_field.append(status2)

        elif threshold_pointer == 3:

            # get the temperature values from the sliders and convert to strings for display
            temperatures = self.getslidervalue()
            temp1 = temperatures[0]
            temp1str = str(temp1)
            temp2 = temperatures[1]
            temp2str = str(temp2)
            # convert the temperature values to threshold 16-Bit values
            threshold1 = thirdmode(temp1)
            threshold1str = str(threshold1)
            threshold2 = thirdmode(temp2)
            threshold2str = str(threshold2)
            # append log window
            self._browse_status.append(
                "Der erste Threshold wurde auf " + threshold1str + "°C (" + threshold1str + " dn) gesetzt")
            self._browse_status.append(
                "Der zweite Threshold wurde auf " + threshold2str + "°C (" + threshold2str + " dn) gesetzt")
            self._browse_status.append("Klassifikation wird gestartet.")
            # get img_input and txt_input
            img_input = readImages(filePath)
            txt_input = readTxt(filePath)
            # check if img_input and txt_input have the same amount of members
            if checkEqualLength(img_input, txt_input):
                # if true - check if the names of the files are identical
                if checkEqualNames(filePath):
                    # if true - start classification
                    acml_list_1 = []
                    acml_list_2 = []
                    self.createthread(img_input, txt_input, threshold1, threshold2, acml_list_1, acml_list_2, temp1,
                                      temp2, outputPath)
                else:
                    # if false - stop
                    self._status_field.append(status4)
            else:
                # if false- stop
                self._status_field.append(status3)
            # after finishing classification - append status to signal finish to user
            self._status_field.append(status2)


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(960)
widget.setFixedHeight(1000)
widget.show()
sys.exit(app.exec_())
