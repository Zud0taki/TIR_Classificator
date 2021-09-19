# defining the camera mode functions

# definition of the first camera mode function
def firstmode(temp):
    x = temp + 273.15
    threshold = x * 100
    return threshold

# definition of the second camera mode function
def secondmode(temp):
    x = temp + 273.15
    threshold = x * 50
    return threshold

# definition of the third camera mode function
def thirdmode(temp):
    x = temp + 273.15
    threshold = ((1 / 3) * x) * (100 / 3)
    return threshold
