from ShapeWriter import *
def export(acml_list, threshold, temperature, outputpath):
    with open('Shapefile.txt', 'w') as f:
        for item in acml_list:
            f.write("%s\n" % item)
    ShapeWrite(acml_list, threshold, temperature, outputpath)