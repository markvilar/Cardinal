import npd
import utilities

import csv

def format_data(input_path: str, output_directory: str, entries: dict):
    csv_data = {}

    for key in entries:
        csv_data[key] = []

    with open(input_path, "r") as file:
        line_total = len(file.readlines())

    with open(input_path, "r") as file:
        for line_count in range(line_total):
            line = npd.Line(file.readline())
            for key, (id, separators) in entries.items():
                # Check if line is valid entry.
                if line.has_id(id) and line.get_data_count() >= 3:
                    # Convert the line into an entry.
                    entry = npd.Entry(id, separators, line)

                    # Get data and timestamp from entry.
                    data = entry.get_data()
                    timestamp = npd.Timestamp(entry.get_time())

                    # Add time and epoch to data.
                    data.insert(0, timestamp.get_epoch())
                    data.insert(0, timestamp.get_time())

                    # Add data to dictionary.
                    csv_data[key].append(data)

            utilities.progress_bar(line_count / line_total * 100)
    
    # Save data.
    print()
    for key, rows in csv_data.items():
        print("{0}: {1},{2}".format(key, len(rows), len(rows[0])))
        input_file = input_path.split("/")[-1].split(".")[0]
        output_path = output_directory + "/" + input_file + "-" + key + ".csv"
        
        # Write to csv.
        with open(output_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            for row in rows:
                writer.writerow(row)

def main():
    path = "./Data/20210122_100221_G.NPD"
    output_directory = "./Output"
    entries = {
        # Title: ( ID, Separators )
        "Vessel-GPS" :         ( "R44  0",         ["  ", ","]        ),
        "Vessel-Gyrocompass" : ( "R104  3",        ["  ", ","]        ),
        "ROV-Gyrocompass" :    ( "R132  4",        ["  ", ","]        ),
        "ROV-HPR" :            ( "R496  10",       ["  ", ","]        ),
        "ROV-HiPAP-HPR" :      ( "P  D   3",       ["   ", "  "]      ),
        "ROV-Digiquartz" :     ( "D     3  19  1", ["   ", "  ", " "] ),
    }

    format_data(path, output_directory, entries)

if __name__ == "__main__":
    main()