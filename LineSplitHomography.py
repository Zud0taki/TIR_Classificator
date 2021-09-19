# import necessary libraries and functions
import numpy as np
from Homography import *

# define lineSplitHomography
# used to split the txt-file and get the corner-real-world-coordinates
def lineSplitHomography(file_in, img):
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

    pts_dst = np.array(
        [[float(x1), float(y1)], [float(x2), float(y2)], [float(x3), float(y3)], [float(x4), float(y4)]])
    h = homographyofpicture(img, pts_dst)
    return h