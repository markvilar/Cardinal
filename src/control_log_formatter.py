from datetime import datetime

import pandas as pd

from file_utils import FileReader, TableReader
from geodesic import latlon_to_utm, utm_to_latlon

def format_date_time(input_time, input_format, output_format):
    date_time = datetime.strptime(input_time, input_format)
    timestamp = datetime.timestamp(date_time)
    date_string = date_time.strftime(output_format)
    return timestamp, date_string

def main():
    # Directories and files
    input_dir = "/home/martin/pCloudDrive/research/data/20160121-kvadehuken/" \
        + "control/"
    input_file = "20160121-1829raw_data.log"

    output_dir = "/home/martin/pCloudDrive/research/data/20160121-kvadehuken/" \
        + "processed/"
    output_file = "20160121-1829-rov-control.csv"

    print("Input dir.:   {}".format(input_dir))
    print("Input file.:  {}".format(input_file))
    print("Output dir.:  {}".format(output_dir))
    print("Output file.: {}".format(output_file))

    # Dataset specific
    date = "2016-01-21"
    utm_zone = 33
    utm_hemi = 'N'

    file_path = input_dir + input_file

    reader = FileReader(file_path, skip_header=True)

    rov_layout = {
        "time"      : ( 0,   str ),
        "northing"  : ( 1, float ),
        "easting"   : ( 2, float ),
        "depth"     : ( 3, float ),
        "heading"   : ( 6, float ),
        }

    rov_table_reader = TableReader(rov_layout)
    while not reader.is_end_of_file():
        line = reader.read_line()
        rov_table_reader.format_entry(line, "\t")

    # Create pandas data frame
    rov_data = rov_table_reader.get_data()
    rov_df = pd.DataFrame.from_dict(rov_data)

    # Filter out the ROV data points without position measurements
    rov_df = rov_df.loc[rov_df["northing"] != 0]
    rov_df = rov_df.loc[rov_df["easting"] != 0]

    # Calculate latitude/longitude
    rov_df["utm_zone"] = utm_zone
    rov_df["utm_hemi"] = utm_hemi
    rov_df[["latitude", "longitude"]] = rov_df.apply(lambda row : \
        utm_to_latlon(row['easting'], row['northing'], row['utm_zone'], 
            row['utm_hemi']), 
        axis = 1,
        result_type ='expand')

    # Process timestamp and datetime
    rov_df["date"] = date
    rov_df[["timestamp", "datetime"]] = rov_df.apply(lambda row : \
        format_date_time(row["date"] + "-" + row["time"], 
            "%Y-%m-%d-%H:%M:%S.%f", 
            "%Y:%m:%d:%H:%M:%S.%f"),
        axis = 1,
        result_type ='expand')

    # Remove separate time and date columns
    rov_df = rov_df.drop(columns=["time", "date"])

    # Save to file
    rov_df.to_csv(output_dir + output_file, index=False, header=True)

if __name__ == "__main__":
    main()
