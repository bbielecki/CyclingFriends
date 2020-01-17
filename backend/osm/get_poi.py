from OSMPythonTools.overpass import Overpass
overpass = Overpass()


def get_poi(lat, lng, radius=50, max_nodes=None):
    result = overpass.query(f'node(around: {radius}, {lat}, {lng});out;')
    filtered_result = list()
    for i in result.elements():
        if i.tags() is not None:
            filtered_result.append(i)
    if max_nodes is not None:
        return filtered_result[:max_nodes]
    else:
        return filtered_result
