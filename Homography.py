import cv2
import numpy as np
import requests
import time
import srtm


srtm_data = srtm.get_data()

def HomographyOfPicture(img_src, pts_dst):
    srcshape = img_src.shape
    # Four corners of the src_img in pxl
    pts_src = np.array([[0, 0], [srcshape[1], 0], [srcshape[1], srcshape[0]], [0, srcshape[0]]])
    # pts_dst = np.array([[53.27451389, 11.17915012], [53.26655878, 11.17956069], [53.26653019, 11.17806564], [53.27448475, 11.17764306]])
    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)
    return h


def HomographyPoints(h, boundary_points):
    # multiplication of the matrices
    transformed_boundary_points = []
    for x in range(len(boundary_points)):
        #TODO Hop through coordinates of boundary_points and replace the 194, 81
        xout = np.matmul(h, [boundary_points[x][1], boundary_points[x][0], 1])
        xout /= xout[2]
        # get height via SRTM
        lat = xout[0]
        long = xout[1]
        height = srtm_data.get_elevation(lat, long)
        # response = requests.get(f"https://api.opentopodata.org/v1/srtm90m?locations={lat},{long}&interpolation=cubic")
        transformed_boundary_points.append([lat, long, height])
    # test = response.text
    return transformed_boundary_points
