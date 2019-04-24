#
# Name: Rachael Bogdany
#       Shannon Quinn
#       Lian Wong
# Filename: GPS_to_KML.py
# Date: 3/25/2019
# Description:
#

import GPS_to_CostMap

def addHeader(filename):
    """
    Adds the header to the decision tree program
    :param filename: File name of the program writing to
    :return: none
    """
    header = ''
    header += '<?xml version = "1.0" encoding = "UTF-8"?>\n'
    header += '<kml xmlns = "http://www.opengis.net/kml/2.2">\n'
    header += '<Document>\n'
    header += '\t<Style id = "yellowPoly">\n'
    header += '\t\t<LineStyle>\n'
    header += '\t\t\t<color> Af00ffff </color>\n'
    header += '\t\t\t<width>6</width>\n'
    header += '\t\t</LineStyle>\n'
    header += '\t\t<PolyStyle>\n'
    header += '\t\t\t<color>7f00ff00</color>\n'
    header += '\t\t</PolyStyle>\n'
    header += '\t</Style>\n'

    filename.write(header)


def convert(gpsfile):
    """
    takes a gps file and coverts the points to a list
    :param gpsfile: gps file pointer
    :return: list of coordinates
    """
    coordinates = []
    lst = []
    for line in gpsfile:
        if line.startswith('$GPGGA'):
            # get time, fix signal and dilution of precision
            arr = line.split(',')
            data = [arr[2], arr[6], arr[8]]
            lst.append(data)

        elif line.startswith('lng'):
            # get longitude, latitude, altitude, speed, angle
            arr = line.split(',')
            lng = arr[0].split('=')
            lng = lng[1]
            lat = arr[1].split('=')
            lat = lat[1]
            alt = arr[2].split('=')
            alt = alt[1]
            speed = arr[3].split('=')
            speed = speed[1]
            ang = arr[5].split('=')
            ang = ang[1]
            lst.append([float(lng), float(lat), float(alt), float(speed), float(ang)])

            # check if a GPGGA line was found, otherwise don't add this point
            if len(lst) == 2:
                coordinates.append(lst)
            lst = []

    return coordinates


def write_coordinates(coordinate_lst, file):
    """
    writes a list of coordinates to a kml file
    :param coordinate_lst: list of coordinates to write to the file
    :param file: kml file pointer
    :return: None
    """
    program = ''
    program += '\t<Placemark>\n'
    program += '\t<styleUrl>#yellowPoly</styleUrl>\n'
    program += '\t<LineString>\n'
    program += '\t\t<Description>Speed in Knots, instead of altitude.</Description>\n'
    program += '\t\t<extrude>1</extrude>\n'
    program += '\t\t<tesselate>1</tesselate>\n'
    program += '\t\t<altitudeMode>absolute</altitudeMode>\n'
    program += '\t\t<coordinates>\n'

    for c in coordinate_lst:
        program += ("\t\t\t" + str(c[0]) + "," + str(c[1]) + "," + str(c[2]) + '\n')

    program += '\t\t</coordinates>\n'
    program += '\t</LineString>\n'
    program += '\t</Placemark>\n'

    file.write(program)

def addTrailer(file):
    """
    Adds the loop to the file that contains the classifier program
    :param file: file
    :return: none
    """
    program = ''
    program += '</Document>\n'
    program += '</kml>\n'
    file.write(program)


def main():
    """
    Main program to run the trainer program
    :return: none
    """
    filename = 'KML_Filename.kml'
    gps_filename = 'data/gps_1.txt'
    gpsfile = open(gps_filename, 'r')
    file = open(filename, 'w')
    addHeader(file)
    coordinate_lst = convert(gpsfile)
    cleaned = GPS_to_CostMap.clean_gps_data(coordinate_lst)
    write_coordinates(cleaned, file)
    addTrailer(file)
    file.close()

if __name__ == '__main__':
    main()