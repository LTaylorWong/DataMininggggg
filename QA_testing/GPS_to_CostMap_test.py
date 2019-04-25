"""
filename: GPS_to_CostMap.py
names: Rachael Bogdany
       Shannon Quinn
       Lian Wong
"""
import GPS_to_KML


def clean_gps_data(data):
    """
    cleans and parses the gps data
    :param data: file pointer to gps data
    :return: cleaned data
    """
    cleaned = []
    i = 0
    for d in data:
        gga = d[0]
        coordinate = d[1]
        fix = int(gga[1])
        precision = gga[2]
        if (fix <= 2 and fix != 0) and (float(precision) <= 4 and float(precision) != 0):
            coordinate.append(gga[0])
            if i % 10 == 0:
                cleaned.append(coordinate)
                # 79494 7917
                clean_redundant(cleaned, coordinate)
        i += 1
    print(len(data), len(cleaned))
    return cleaned


def clean_redundant(cleaned, coordinate):
    if len(cleaned) > 0:
        last = cleaned[len(cleaned) - 1]
        lng = coordinate[0]
        lon = coordinate[1]
        if abs(last[0] - lng) >= 0.001 or abs(last[1] - lon) >= 0.001:
                cleaned.append(coordinate)
    else:
        cleaned.append(coordinate)


def classify_coordinates(coordinates):
    """
    classifies where stops, left turns and right turns occurred
    :param coordinates: list of coordinates
    :return: list of classified points
    """

    classified_coordinates = []
    right_class = []
    left_class = []

    for i in range(1, len(coordinates) - 1):
        lng = coordinates[i][0]
        lon = coordinates[i][1]
        speed = coordinates[i][3]

        prev_lng = coordinates[i - 1][0]
        prev_lon = coordinates[i - 1][1]
        prev_speed = coordinates[i - 1][3]

        next_lng = coordinates[i + 1][0]
        next_lon = coordinates[i + 1][1]
        next_speed = coordinates[i + 1][3]

        lng_threshold = abs(lng - prev_lng) <= 0.0005 and abs(lng - next_lng) <= 0.0005
        lon_threshold = abs(lon - prev_lon) <= 0.0005 and abs(lon - next_lon) <= 0.0005
        speed_threshold = speed <= 0.1 and prev_speed <= 0.1 and next_speed <= 0.1

        if lng_threshold and lon_threshold and speed_threshold:
            # print("Classified stop at", lng, lon, speed)
            redundant_data_check(lng, lon, classified_coordinates, 's')

        turn_ang_before = coordinates[i - 1][4]
        turn_ang_after = coordinates[i + 1][4]
        answer = turn_ang_after - turn_ang_before

        if answer >= 65 and answer <= 115:
            print("Classified right", answer, turn_ang_before, turn_ang_after)
            right_class.append([(lng, lon), 'r'])
            redundant_data_check(lng, lon, classified_coordinates, 'r')
        elif answer <= -65 and answer >= -120:
            left_class.append([(lng, lon), 'l'])
            redundant_data_check(lng, lon, classified_coordinates, 'l')
            print("Classified left", answer, turn_ang_before, turn_ang_after)

    return classified_coordinates


def redundant_data_check(lng, lon, classified, group):
    """
    checks if a data point within a certain threshold has already been classified in the set
    helps to avoid writing too many points in one spot if they were there too long
    :param lng: current longitude
    :param lon: current longitude
    :param classified: list of points already classified
    :param group: classification
    :return: None
    """
    if len(classified) > 0:
        last = classified[len(classified) - 1]
        if (abs(float(last[0][0]) - lng) >= 0.001 or abs(float(last[0][1]) - lon) >= 0.001) and group != last[1]:
                classified.append([(lng, lon), group])

    else:
        classified.append([(lng, lon), group])


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

    if direction == 'l':
        file.write(indent + "<description> Red Pin for left turn, %f,%f </description>\n" % (coordinate[0], coordinate[1]))
        file.write(indent + '<styleUrl>#redLeftMark</styleUrl>\n')
    elif direction == 'r':
        file.write(indent + "<description> Green Pin for right turn %f,%f </description>\n" % (coordinate[0], coordinate[1]))
        file.write(indent + '<styleUrl>#greenRightMark</styleUrl>\n')
    else:
        file.write(indent + "<description> Yellow Pin for stop %f,%f </description>\n" % (coordinate[0], coordinate[1]))
        file.write(indent + '<styleUrl>#yellowStopMark</styleUrl>\n')

    file.write(indent + "<Point>\n")
    file.write(indent * 2)
    file.write("<coordinates>%f,%f</coordinates>\n" % (coordinate[0], coordinate[1]))
    file.write(indent + "</Point>\n")
    file.write("</Placemark>\n")


def main():

    gps_file = 'gps_1.txt'

    gps_f = open(gps_file)
    gps_data = GPS_to_KML.convert(gps_f)
    gps_f.close()

    coors = clean_gps_data(gps_data)

    classified = classify_coordinates(coors)

    kml_path = "cost_map_out.kml"
    with open(kml_path, 'w') as f:
        top_kml(f)
        for c in classified:
            write_coordinate(c[0], f, c[1])
        end_kml(f)


if __name__ == '__main__':
    main()
