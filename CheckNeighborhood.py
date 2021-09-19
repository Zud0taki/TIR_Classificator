# define checknbh - checking the neighborhood of labeled pixels
def checknbh(img, label_mat, label, threshold, x, y):
    new_coords = [x, y]
    label_mat[y, x] = label
    # as long as the new_coords list is not zero = active -> check coordinates -> index and label them -> delete list with indices
    while not len(new_coords) == 0:
        indexX = len(new_coords) - 2
        indexY = len(new_coords) - 1
        checkX = new_coords[indexX]
        checkY = new_coords[indexY]
        del new_coords[indexX:]
        label_mat[y, x] = label
        # check in the neighborhood of 3x3 pixels
        for i in range(3):
            for j in range(3):
                currX = checkX - 1 + i
                currY = checkY - 1 + j
                # check if pixel is possible (border-check)
                if currX < 0 or currX > (img.shape[1] - 1) or currY < 0 or currY > (img.shape[0] - 1):
                    isborder = True
                else:
                    isborder = False
                # check if pixel is not out of bounds and pixel exceeds threshold and pixel is not already labeled
                if not isborder and img[currY, currX] > threshold and label_mat[currY, currX] < 1:
                    checkTresh = img[currY, currX]
                    checkLabel = label_mat[currY, currX]
                    label_mat[currY, currX] = label
                    new_coords.append(currX)
                    new_coords.append(currY)
        # return the label matrix
    return label_mat