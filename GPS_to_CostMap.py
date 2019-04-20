"""
filename: GPS_to_CostMap.py
names: Rachael Bogdany
       Shannon Quinn
       Lian Wong
"""


def clean_gps_data(file):
    """
    cleans and parses the gps data
    :param file: file pointer to gps data
    :return: cleaned data
    """

    for _ in range(5):
        next(file)

    for i in file:
        print(i)
        print("END")


def top_kml(file):
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    file.write('<Document>\n')


def end_kml(file):
    file.write('</Document>\n')
    file.write('</kml>\n')


def write_coordinate(coordinate, file, direction):
    """
    writes a coordinate to the kml file
    :param coordinate: coordinate where the right turn happens
    :param file: kml file pointer
    :param direction: determines what color flag to places
        left -> red flag, right -> green flag, stop -> yellow flag
    :return: None
    """

    indent = "    "
    half_indent = "  "
    red = 'BB0B27'
    green = '005900'
    yellow = 'FFCA00'

    file.write("<Placemark>\n")

    if direction == 'left':
        file.write(indent + "<description> Red Pin for left turn </description>\n")
    elif direction == 'right':
        file.write(indent + "<description> Green Pin for right turn </description>\n")
    else:
        file.write(indent + "<description> Yellow Pin for stop </description>\n")

    file.write(indent + '<Style id="normalPlacemark">\n')
    file.write(indent + half_indent + "<IconStyle>\n")

    if direction == 'left':
        file.write(indent * 2 + "<color>%s</color>\n" % red)
    elif direction == 'right':
        file.write(indent * 2 + "<color>%s</color>\n" % green)
    else:
        file.write(indent * 2 + "<color>%s</color>\n" % yellow)

    file.write(indent * 2 + "<Icon>\n")
    file.write(indent * 2 + half_indent + "<href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>\n")
    file.write(indent * 2 + "</Icon>\n")
    file.write(indent + half_indent + "</IconStyle>\n")
    file.write(indent + "</Style>\n")
    file.write(indent + "<Point>\n")
    file.write(indent * 2)
    file.write("<coordinates>%f,%f</coordinates>\n" % (coordinate[0], coordinate[1]))
    file.write(indent + "</Point>\n")
    file.write("</Placemark>\n")


def main():
    # file = input()
    # with open(file) as f:
    #     clean_gps_data(f)

    # some test coordinates for file writing
    kml_path = "cost_map.kml"
    with open(kml_path, 'w') as f:
        top_kml(f)
        write_coordinate((-77.59, 43.13), f, "left")
        write_coordinate((-77.50, 43.10), f, "right")
        write_coordinate((-77.60, 43.12), f, "stop")
        end_kml(f)


if __name__ == '__main__':
    main()