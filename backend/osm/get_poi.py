from OSMPythonTools.overpass import Overpass
overpass = Overpass()

def get_poi(lat, lon):
    result = overpass.query(f'node(around: 50, {lat}, {lon});out;')
    filtered_result = list()
    for i in result.elements():
        if i.tags() is not None:
            filtered_result.append(i)

    return filtered_result