"""
filename: GPS_to_CostMap.py
names: Rachael Bogdany
       Shannon Quinn
       Lian Wong
"""
import numpy as np
import csv


def clean_gps_data(file):
    """
    cleans and parses the gps data
    :param file: file pointer to gps data
    :return: cleaned data
    """
    for i in range(5, len(file)):
        print(file[i])


def left_turn_coordinate(coordinate, file):
    """
    writes a left turn coordinate to the appropriate kml file
    :param coordinate: coordinate where the right turn happens
    :param file: kml file pointer
    :return: None
    """
    pass


def right_turn_coordinate(coordinate, file):
    """
    writes a right turn coordinate to the appropriate kml file
    :param coordinate: coordinate where the right turn happens
    :param file: kml file pointer
    :return: None
    """
    pass


def stop_coordinate(coordinate, file):
    """
    writes a stop coordinate to the appropriate kml file
    :param coordinate: coordinate where the right turn happens
    :param file: kml file pointer
    :return: None
    """
    pass


def main():
    file = input()
    with open(file) as f:
        f = csv.reader(f)
        clean_gps_data(f)


if __name__ == '__main__':
    main()