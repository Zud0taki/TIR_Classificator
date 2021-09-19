# import necessary libraries
import cv2
import numpy as np
import requests
import time
import srtm

# load srtm data
srtm_data = srtm.get_data()

# define homographyofpicture
# used to calculate the homography of the given picture
def homographyofpicture(img_src, pts_dst):
    srcshape = img_src.shape
    # Four corners of the src_img in pxl
    pts_src = np.array([[0, 0], [srcshape[1], 0], [srcshape[1], srcshape[0]], [0, srcshape[0]]])
    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)
    return h

# define homographypoints
# used to transform boundary points into real world coordinates
def homographypoints(h, boundary_points):
    # multiplication of the matrices
    transformed_boundary_points = []
    for x in range(len(boundary_points)):
        xout = np.matmul(h, [boundary_points[x][1], boundary_points[x][0], 1])
        xout /= xout[2]
        # get height via SRTM
        lat = xout[0]
        long = xout[1]
        height = srtm_data.get_elevation(lat, long)
        transformed_boundary_points.append([lat, long, height])
    # test = response.text
    return transformed_boundary_points
