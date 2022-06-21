# Performing Trilateration on a Give 3 Points
import numpy
import pandas as pd
import os
import glob

# Refracance Points GPS

Lat1 = 46.067579
Lon1 = 11.15091679
Lat2 = 46.06816989
Lon2 = 11.1507222
Lat3 = 46.067967
Lon3 = 11.150922


# Hervestine Distance between Lat1/ Lon1 to Lat2/Lon2


def dis_calc_herv(Lat1, Lon1, Lat2=[], Lon2=[]):
    earthR = 6356.137  # in Km

    latA = numpy.radians(Lat1)
    lonA = numpy.radians(Lon1)
    latB = numpy.radians(Lat2)
    lonB = numpy.radians(Lon2)

    dlon = lonB - lonA
    dlat = latB - latA

    a = pow(numpy.sin(dlat / 2), 2) + numpy.cos(latA) * \
        numpy.cos(latB) * pow(numpy.sin(dlon / 2), 2)
    c = 2 * numpy.arctan2(numpy.sqrt(a), numpy.sqrt(1 - a))

    distance = earthR * c

    return distance*pow(10, 3)  # Conv to meters

# Distance between Two Points in XY


def xy_distance(x1, y1, x=[], y=[]):

    # Standard Distance Equation
    radius = numpy.sqrt(pow(x1-x, 2)+pow(y1-y, 2))

    return radius

# Triliterataion XY in meters


def Tri_conv(r1, r2, r3, Time):

    # Refracance UWB Points
    x1 = 118.05
    x2 = 52.49
    x3 = 74.99
    y1 = 50.6
    y2 = 35.6
    y3 = 51.05

    A = 2*x2 - 2*x1
    B = 2*y2 - 2*y1
    C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2*x3 - 2*x2
    E = 2*y3 - 2*y2
    F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)

    new = {
        'time_stamps': Time,
        'x': x,
        'y': y
    }

    l = pd.DataFrame(new)
    return(l)

# Conversion to CAD XY


def Conversion(File_Path, type):
    path = File_Path
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    print(csv_files)

    # loop over the list of csv files
    for i in csv_files:
        # read the csv file
        if(type == "UWB"):
            col_list = ["rosbagTimestamp", "secs", "nsecs", "x", "y", "z"]
            data = pd.read_csv(i, usecols=col_list)
            UWB = pd.DataFrame(Tri_conv(xy_distance(0, 0, data["x"], data["y"]),
                                        xy_distance(-15.15, 65.709,
                                                    data["x"], data["y"]),
                                        xy_distance(0, 43.145, data["x"], data["y"]), data["rosbagTimestamp"]))
            i = i[:i.rfind('.csv')]
            UWB.to_csv(i+"_cad.csv")

        if(type == "GPS"):
            col_list = ["time_us", "lat", "lon"]
            data = pd.read_csv(i, usecols=col_list)
            GPS = pd.DataFrame(Tri_conv(dis_calc_herv(Lat1, Lon1, data["lat"], data["lon"]),
                                        dis_calc_herv(
                                            Lat2, Lon2, data["lat"], data["lon"]),
                                        dis_calc_herv(Lat3, Lon3, data["lat"], data["lon"]), data["time_us"]))
            i = i[:i.rfind('.csv')]
            GPS.to_csv(i+"_cad.csv")


# Function Invoked when Given Path and type of Conversion
Conversion("/Users/anasosman/Downloads/Experiment2/RoundTrip/Without_Offset", "UWB")
