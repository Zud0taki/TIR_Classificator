import fiona


def ShapeWrite(acml_list, threshold, temperature, outputPath):
    polygon_name = r"" + outputPath + "/" + str(threshold) + "dn - " + str(temperature) + "°C" + ".shp"
    xy_list = []
    schema = {
        'geometry': 'Polygon',
        'properties': [('Name', 'str')]
    }
    polyShp = fiona.open(polygon_name, mode='w', driver='ESRI Shapefile',
                         schema=schema, crs="WGS84")
    label_counter = 1
    for x in range(len(acml_list)):
        if acml_list[x][0][0] != 0:
            xy_list.append((acml_list[x][1][1], acml_list[x][1][0]))
        else:
            label_counter += 1
            polygon_id = str(label_counter)
            # save record and close shapefile
            rowDict = {
                'geometry': {'type': 'Polygon',
                             'coordinates': [xy_list]},  # Here the xyList is in brackets
                'properties': {'Name': polygon_id},
            }
            polyShp.write(rowDict)
            xy_list.clear()
    polyShp.close()
