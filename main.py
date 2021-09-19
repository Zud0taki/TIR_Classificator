# import necessary libraries and functions
from GUI import *
from FullClassification import *


# define the run method
# used to start the process
def run(self, filepath, threshold, temperature, outputpath):
    # create Object from FullClassificator
    FullClassificatorObj = FullClassificator()
    # initialize returnlist
    returnlist = []
    returnlist.clear()
    # read inputs
    img_input = readImages(filepath)
    txt_input = readTxt(filepath)
    # check the equal length of the inputs
    if checkEqualLength(img_input, txt_input):
        # check the equality of the names
        if checkEqualNames(filepath):
            # if both true - start classification
            acml_list = []
            FullClassificatorObj.processPicture(img_input, txt_input, threshold, returnlist, acml_list, temperature, outputpath)

