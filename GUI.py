import sys
from main import *
from PyQt5 import QtWidgets
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from main import main
from CameraModes import *


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        loadUi("Classificator.ui", self)
        self.FClassificator = main()
        self._browse_files_btn.clicked.connect(self.browseimages)
        self._browse_output_btn.clicked.connect(self.browseoutput)
        self._start_btn.clicked.connect(self.startclassification)
        self._threshold_slider.sliderMoved.connect(self.getslidervalue)
        self._threshold_slider_2.sliderMoved.connect(self.getslidervalue)
        self._profile1_radio.toggled.connect(lambda: self.checkradiostate(self._profile1_radio))
        self._profile2_radio.toggled.connect(lambda: self.checkradiostate(self._profile2_radio))
        self._profile3_radio.toggled.connect(lambda: self.checkradiostate(self._profile3_radio))
        self._classificationb_selection_combox.currentIndexChanged.connect(self.getcombovalue)

    def getcombovalue(self):
        ComboValue = self._classificationb_selection_combox.currentIndex()
        # print(ComboValue)
        return ComboValue

    def loggingDisplay(self, message):
        self._status_display.append(message)

    def checkforthresh(self):
        threshold_pointer = 0
        if self._profile1_radio.isChecked():
            threshold_pointer = 1
            return threshold_pointer
        if self._profile2_radio.isChecked():
            threshold_pointer = 2
            return threshold_pointer
        if self._profile3_radio.isChecked():
            threshold_pointer = 3
            return threshold_pointer

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

    def getslidervalue(self):
        threshold = self._threshold_slider.value()
        th = str(threshold)
        self._thresholdv_label.setText(th)
        threshold2 = self._threshold_slider_2.value()
        th2 = str(threshold2)
        self._thresholdv_label_2.setText(th2)
        thresholds = [threshold, threshold2]
        return thresholds

    def getpaths(self):
        imgpath = r"" + self._filename_input.text()
        outputPath = r"" + self._output_input.text()
        pathlist = [imgpath, outputPath]
        return pathlist

    def browseoutput(self):
        outputpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Output Folder')
        self._output_input.setText(outputpath)

    def browseimages(self):
        imgpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Image Folder')
        self._filename_input.setText(imgpath)

    def startclassification(self):

        status1 = "Status des Klassifikators: Running"
        status2 = "Status des Klassifikators: Berechnung des ersten Threshold erfolgreich."
        status3 = "Status des Klassifikators: Berechnung des zweiten Threshold erfolgreich"
        status4 = "Status des Klassifikators: Beendet"

        comboValue = self.getcombovalue()
        if comboValue == 0:
            print("Volle Klassifikation")
        elif comboValue == 1:
            print("Only Threshold")

        self._status_field.append(status1)
        QTest.qWait(1000)
        pathlist = self.getpaths()
        temperatures = self.getslidervalue()

        th1 = temperatures[0]
        th1str = str(th1)
        th2 = temperatures[1]
        th2str = str(th2)

        filePath = pathlist[0]
        outputPath = pathlist[1]

        threshold_pointer = self.checkforthresh()
        if threshold_pointer == 0:
            self._browse_status.append("Es wurde kein Kameramodus gewählt.")
        elif threshold_pointer == 1:
            threshold1 = firstmode(th1)
            threshold1str = str(threshold1)
            self._browse_status.append(
                "Der erste Threshold wurde auf " + th1str + "°C (" + threshold1str + " dn) gesetzt")
            log1 = main(filePath, threshold1, outputPath)
            for x in log1:
                self._browse_status.append(x)
            self._status_field.append(status2)
            QTest.qWait(1000)
            threshold2 = firstmode(th2)
            threshold2str = str(threshold2)
            self._browse_status.append(
                "\n" + "============================================================================================" + "\n" + "Der zweite Threshold wurde auf " + th2str + "°C (" + threshold2str + " dn) gesetzt")
            log2 = main(filePath, threshold2, outputPath)
            for y in log2:
                self._browse_status.append(y)
            self._status_field.append(status3)
            self._status_field.append(status4)

        elif threshold_pointer == 2:
            threshold1 = secondmode(th1)
            threshold1str = str(threshold1)
            self._browse_status.append(
                "Der erste Threshold wurde auf " + th1str + "°C (" + threshold1str + " dn) gesetzt")
            self.FClassificator.trigger.connect(self.getandwritelog)
            self.FClassificator.run(filePath, threshold1, th1, outputPath)
            #log1 = main(filePath, threshold1, th1, outputPath)
            # for x in log1:
            #     self._browse_status.append(x)
            # self._status_field.append(status2)
            # QTest.qWait(1000)
            # threshold2 = secondmode(th2)
            # threshold2str = str(threshold2)
            # self._browse_status.append(
            #     "\n" + "============================================================================================" + "\n" + "Der zweite Threshold wurde auf " + th2str + "°C (" + threshold2str + " dn) gesetzt")
            # #log2 = main(filePath, threshold2, th2, outputPath)
            # for y in log2:
            #     self._browse_status.append(y)
            # self._status_field.append(status3)
            # self._status_field.append(status4)

        elif threshold_pointer == 3:
            threshold1 = thirdmode(th1)
            threshold1str = str(threshold1)
            self._browse_status.append(
                "Der erste Threshold wurde auf " + th1str + "°C (" + threshold1str + " dn) gesetzt")
            log1 = main(filePath, threshold1, outputPath)
            for x in log1:
                self._browse_status.append(x)
            self._status_field.append(status2)
            QTest.qWait(1000)
            threshold2 = thirdmode(th2)
            threshold2str = str(threshold2)
            self._browse_status.append(
                "\n" + "============================================================================================" + "\n" +
                "Der zweite Threshold wurde auf " + th2str + "°C (" + threshold2str + " dn) gesetzt")
            log2 = main(filePath, threshold2, outputPath)
            for y in log2:
                self._browse_status.append(y)
            self._status_field.append(status3)
            self._status_field.append(status4)

    def getandwritelog(self):
        self._browse_status.append(self.FClassificator.logstring)
        cv.waitKey()


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(960)
widget.setFixedHeight(1000)
widget.show()

sys.exit(app.exec_())
