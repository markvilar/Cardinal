import csv

from datetime import datetime
from functools import partial
from typing import Dict

import pandas as pd

from geodesic import latlon_to_utm

def format_vessel_gps(data : Dict, buffer : str):
    buffer_entries = buffer.split()

    id      = buffer_entries[0]
    index   = buffer_entries[1]
    date    = buffer_entries[2]
    message = buffer_entries[3]

    timestamp = datetime.timestamp(datetime.strptime(date, 
        "%Y:%m:%d:%H:%M:%S.%f"))

    message_entries = message.split(",")

    latitude    = float(message_entries[2])
    north_south = message_entries[3]
    longitude   = float(message_entries[4])
    east_west   = message_entries[5]

    latitude_deg = int(latitude / 100)
    latitude_min = int(latitude % 100)
    latitude_sec = (latitude % 1) * 60

    longitude_deg = int(longitude / 100)
    longitude_min = int(longitude % 100)
    longitude_sec = (longitude % 1) * 60

    latitude = latitude_deg + latitude_min / 60 + latitude_sec / 3600
    longitude = longitude_deg + longitude_min / 60 + longitude_sec / 3600

    northing, easting, utm_zone, utm_hemi = latlon_to_utm(latitude, longitude)

    data_headers = [
        "date", 
        "timestamp", 
        "latitude", 
        "north_south", 
        "longitude",
        "east_west",
        "northing",
        "easting",
        "utm_zone",
        "utm_hemi",
        ]
    
    for header in data_headers:
        if not header in data:
            data[header] = []

    data["date"].append(date)
    data["timestamp"].append(timestamp)
    data["latitude"].append(latitude)
    data["north_south"].append(north_south)
    data["longitude"].append(longitude)
    data["east_west"].append(east_west)
    data["northing"].append(northing)
    data["easting"].append(easting)
    data["utm_zone"].append(utm_zone)
    data["utm_hemi"].append(utm_hemi)

def format_vessel_gyro(data : Dict, buffer : str):
    pass

def format_rov_aps(data : Dict, buffer : str):
    buffer_entries = buffer.split()

    id      = buffer_entries[0]
    index   = buffer_entries[1]
    date    = buffer_entries[2]
    message = buffer_entries[3]

    timestamp = datetime.timestamp(datetime.strptime(date, 
        "%Y:%m:%d:%H:%M:%S.%f"))

    message_entries = message.split(",")

    transducer_id = message_entries[2]
    transducer_status = message_entries[3]
    error_code = message_entries[4]
    coordinate_system = message_entries[5]

    if error_code != "":
        return

    x_coordinate = float(message_entries[8])
    y_coordinate = float(message_entries[9])
    z_coordinate = float(message_entries[10])

    data_headers = [
        "date", 
        "timestamp", 
        "trans_id",
        "trans_status",
        "coord_sys",
        "x_coord",
        "y_coord",
        "z_coord",
        ]

    for header in data_headers:
        if not header in data:
            data[header] = []

    data["date"].append(date)
    data["timestamp"].append(timestamp)
    data["trans_id"].append(transducer_id)
    data["trans_status"].append(transducer_status)
    data["coord_sys"].append(coordinate_system)
    data["x_coord"].append(x_coordinate)
    data["y_coord"].append(y_coordinate)
    data["z_coord"].append(z_coordinate)

def format_rov_gyro(data : Dict, buffer : str):
    pass


def main():
    entries = {
        "vessel/gps"  : { 
            "identifier" : "R44", 
            "formatter"  : format_vessel_gps,
            "data"       : {},
            },
        "vessel/gyro" : { 
            "identifier" : "R104", 
            "formatter"  : format_vessel_gyro,
            "data"       : {},
            },
        "rov/aps"     : { 
            "identifier" : "R496", 
            "formatter"  : format_rov_aps,
            "data"       : {},
            },
        "rov/gyro"    : { 
            "identifier" : "R132", 
            "formatter"  : format_rov_gyro,
            "data"       : {},
            },
    }

    root_dir = "/home/martin/pCloudDrive/research/data/" \
        + "20160301-tautra/navigation/"
    filepath =  root_dir + "/20160301_124646_G.NPD"

    with open(filepath, "r", encoding="utf8", errors="ignore") as file:
        line_total = len(file.readlines())

    with open(filepath, "r", encoding="utf8", errors="ignore") as file:
        for line_index in range(line_total):
            line = file.readline()
            line_entries = line.split()
            if len(line_entries) == 0:
                continue
            else:
                line_start = line_entries[0]
                for key in entries.keys():
                    if line_start == entries[key]["identifier"]:
                        entries[key]["formatter"](entries[key]["data"], line)
    
    # Write csv
    df = pd.DataFrame.from_dict(entries["vessel/gps"]["data"]) 
    df.to_csv(root_dir + "vessel_gps.csv", index = False, header=True)

    df = pd.DataFrame.from_dict(entries["rov/aps"]["data"]) 
    df.to_csv(root_dir + "rov_aps.csv", index = False, header=True)

if __name__ == '__main__':
    main()
