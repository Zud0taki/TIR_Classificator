# import necessary libraries
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from ConcaveHull import ConcaveHull

# create ConcaveHull-Object ch -> calculate hull from loaded points
ch = ConcaveHull()
pts = np.random.uniform(size=(100, 2))
ch.loadpoints(pts)
ch.calculatehull()
boundary_points = np.vstack(ch.boundary.exterior.coords.xy).T

# hop through points and color them blue
for y in pts:
    plt.scatter(y[0], y[1], color='blue')
# hop through boundary_points and color them red
for x in boundary_points:
    plt.scatter(x[0], x[1], color='red')
# show results
plt.show()
# boundary_points is a subset of pts corresponding to the concave hull