import cv2 as cv


with open('Streifen4_save_054.txt') as file_in:
    lines = []
    for line in file_in:
        lines.append(line)
    print(lines)
    cv.waitKey()