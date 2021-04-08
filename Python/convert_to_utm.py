import csv

import utm

def main():
    input_path = "./Data/Vessel-GPS.csv"
    output_path = "./Output/Vessel-GPS-UTM.csv"
    input_fields = [ "Datetime", "Epoch", 
        "North Degrees", "North Minutes", "North Seconds",
        "East Degress", "East Minutes", "East Seconds",
        "Latitude", "Longitude" ]
    output_fields = [ "Datetime", "Epoch", "UTM Northing", "UTM Easting", 
        "Zone", "Hemisphere" ]

    with open(input_path, 'r') as input_file, \
        open(output_path, 'w', newline='') as output_file:
        reader = csv.DictReader(input_file, input_fields)
        writer = csv.DictWriter(output_file, output_fields)

        line_count = 0
        for row in reader:
            # Headers.
            if line_count > 0:
                datetime = row["Datetime"]
                epoch = int(row["Epoch"])
                latitude = float(row["Latitude"])
                longitude = float(row["Longitude"])

                [[northing, easting], zone, hemisphere] = utm.LatLonToUtm( \
                    latitude, longitude)

                writer.writerow({
                    "Datetime" : datetime,
                    "Epoch" : epoch,
                    "UTM Northing" : northing, 
                    "UTM Easting" : easting, 
                    "Zone" : zone, 
                    "Hemisphere" : hemisphere
                })

            line_count += 1

if __name__ == '__main__':
    main()
