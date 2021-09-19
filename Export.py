# import functions from ShapeWriter
from ShapeWriter import *


# define export function using accumulated list, threshold value, temperature value and the outputpath
# write Shapefile.txt with the items from the accumulated list
def export(acml_list, threshold, temperature, outputpath):
    with open('Shapefile.txt', 'w') as f:
        for item in acml_list:
            f.write("%s\n" % item)
    ShapeWrite(acml_list, threshold, temperature, outputpath)