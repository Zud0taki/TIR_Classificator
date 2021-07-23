import requests
import cv2 as cv
lat = 53.3
long = 11.2
response = requests.get(f"https://api.opentopodata.org/v1/srtm90m?locations={lat},{long}&interpolation=cubic")
test = response.text
print(test)
height = test.find('elevation')
print(height)
#cv.waitkey()
