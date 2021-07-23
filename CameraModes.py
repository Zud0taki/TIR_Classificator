def firstmode(temp):
    x = temp + 273.15
    threshold = x * 100
    return threshold


def secondmode(temp):
    x = temp + 273.15
    threshold = x * 50
    return threshold


def thirdmode(temp):
    x = temp + 273.15
    threshold = ((1 / 3) * x) * (100 / 3)
    return threshold
