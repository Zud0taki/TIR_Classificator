import numpy as np

def checkLinearity(pts):

    coordinate_1 = np.array(pts[0])
    coordinate_2 = np.array(pts[1])
    direction_vector = coordinate_2 - coordinate_1
    nonlinear = True
    for x in range(1, len(pts) - 1):
       coordinate_1 = np.array(pts[x])
       coordinate_2 = np.array(pts[x+1])
       compare_vector = coordinate_2 - coordinate_1
       if compare_vector[0] == direction_vector[0] and compare_vector[1] == direction_vector[1]:
           nonlinear = False
       else:
           nonlinear = True
           break
    return nonlinear
