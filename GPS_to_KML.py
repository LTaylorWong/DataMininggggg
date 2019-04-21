#
# Name: Rachael Bogdany
#       Shannon Quinn
#       Lian Wong
# Filename: GPS_to_KML.py
# Date: 3/25/2019
# Description:
#

import pandas as pd
import math

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
    header += '\t<Placemark>\n'
    header += '\t<styleUrl>#yellowPoly</styleUrl>\n'
    header += '\t<LineString>\n'
    header += '\t\t<Description>Speed in Knots, instead of altitude.</Description>\n'
    header += '\t\t<extrude>1</extrude>\n'
    header += '\t\t<tesselate>1</tesselate>\n'
    header += '\t\t<altitudeMode>absolute</altitudeMode>\n'
    header += '\t\t<coordinates>\n'
    filename.write(header)

def convert(gpsfile):
    """
    takes a gps file and coverts the points to a list
    :param gpsfile: gps file pointer
    :return: list of coordinates
    """
    coordinates = []
    for line in gpsfile:
        if(line.startswith('lng')):
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
            coordinates.append([float(lng), float(lat), float(alt), float(speed), float(ang)])

    return coordinates

def write_coordinates(coordinate_lst, file):
    """
    writes a list of coordinates to a kml file
    :param coordinate_lst: list of coordinates to write to the file
    :param file: kml file pointer
    :return: None
    """
    for coordinate in coordinate_lst:
        file.write("\t\t\t" + str(coordinate[0]) + "," + str(coordinate[1]) + "," + str(coordinate[2]) +'\n')

def addTrailer(file):
    """
    Adds the loop to the file that contains the classifier program
    :param bestAttribute: str
    :param value: int
    :param file: file
    :return: none
    """
    program = '\t\t</coordinates>\n'
    program += '\t</LineString>\n'
    program += '\t</Placemark>\n'
    program += '</Document>\n'
    program += '</kml>\n'
    file.write(program)

def main():
    """
    Main program to run the trainer program
    :return: none
    """
    filename = 'KML_Filename.kml'
    GPSFilename = 'data/gps_1.txt'
    gpsfile = open(GPSFilename, 'r')
    file = open(filename, 'w')
    addHeader(file)
    coordinate_lst = convert(gpsfile)
    write_coordinates(coordinate_lst, file)
    addTrailer(file)
    file.close()

main()