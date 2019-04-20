"""
filename: GPS_to_CostMap.py
names: Rachael Bogdany
       Shannon Quinn
       Lian Wong
"""
import GPS_to_KML


def clean_gps_data(gps_file):
    """
    cleans and parses the gps data
    :param file: file pointer to gps data
    :return: cleaned data
    """

    coordinate_file = "coordinate.txt"

    gps_f = open(gps_file)
    coordinate_f = open(coordinate_file, 'w')

    GPS_to_KML.convert(gps_f, coordinate_f)


def top_kml(file):
    """
    writes the header for the cost kml file
    adds the style for the different pins needed
    :param file: kml file pointer
    :return: None
    """
    indent = '    '
    half_indent = '  '
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    file.write('<Document>\n')

    for i in range(3):
        if i == 0:
            file.write(indent + "<Style id='redLeftMark'>\n")
        elif i == 1:
            file.write(indent + "<Style id='greenRightMark'>\n")
        else:
            file.write(indent + "<Style id='yellowStopMark'>\n")

        file.write(half_indent + indent + "<IconStyle>\n")
        file.write(indent * 2 + '<Icon>\n')
        if i == 0:
            file.write(
                indent * 2 + half_indent + '<href>http://maps.google.com/mapfiles/kml/paddle/red-stars.png</href>\n')
        elif i == 1:
            file.write(
                indent * 2 + half_indent + '<href>http://maps.google.com/mapfiles/kml/paddle/grn-stars.png</href>\n')
        else:
            file.write(
                indent * 2 + half_indent + '<href>http://maps.google.com/mapfiles/kml/paddle/ylw-stars.png</href>\n')

        file.write(indent * 2 + '</Icon>\n')
        file.write(half_indent + indent + '</IconStyle>\n')
        file.write(indent + '</Style>\n')


def end_kml(file):
    """
    writes end of kml file
    :param file: kml file pointer
    :return: None
    """
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

    file.write("<Placemark>\n")

    if direction == 'left':
        file.write(indent + "<description> Red Pin for left turn </description>\n")
        file.write(indent + '<styleUrl>#redLeftMark</styleUrl>\n')
    elif direction == 'right':
        file.write(indent + "<description> Green Pin for right turn </description>\n")
        file.write(indent + '<styleUrl>#greenRightMark</styleUrl>\n')
    else:
        file.write(indent + "<description> Yellow Pin for stop </description>\n")
        file.write(indent + '<styleUrl>#yellowStopMark</styleUrl>\n')

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
    gps_file = 'gps_1.txt'

    clean_gps_data(gps_file)

    kml_path = "cost_map.kml"
    with open(kml_path, 'w') as f:
        top_kml(f)

        end_kml(f)


if __name__ == '__main__':
    main()
