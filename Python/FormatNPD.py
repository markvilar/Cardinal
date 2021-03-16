import NPD
import Utilities

import csv

def FormatData(inputPath: str, outputDirectory: str, entries: dict):
    csvData = {}

    for key in entries:
        csvData[key] = []

    with open(inputPath, "r") as file:
        lineTotal = len(file.readlines())

    with open(inputPath, "r") as file:
        for lineCount in range(lineTotal):
            line = NPD.Line(file.readline())
            for key, (id, separators) in entries.items():
                # Check if line is valid entry.
                if line.HasID(id) and line.GetDataCount() >= 3:
                    # Convert the line into an entry.
                    entry = NPD.Entry(id, separators, line)

                    # Get data and timestamp from entry.
                    data = entry.GetData()
                    timestamp = NPD.Timestamp(entry.GetTime())

                    # Add time and epoch to data.
                    data.insert(0, timestamp.GetEpoch())
                    data.insert(0, timestamp.GetTime())

                    # Add data to dictionary.
                    csvData[key].append(data)

            Utilities.ProgressBar(lineCount / lineTotal * 100)
    
    # Save data.
    print()
    for key, rows in csvData.items():
        print("{0}: {1},{2}".format(key, len(rows), len(rows[0])))
        inputFile = inputPath.split("/")[-1].split(".")[0]
        outputPath = outputDirectory + "/" + inputFile + "-" + key + ".csv"
        
        # Write to csv.
        with open(outputPath, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            for row in rows:
                writer.writerow(row)

def Main():
    path = "./Data/20210122_100221_G.NPD"
    outputDirectory = "./Output"
    entries = {
        "Pri-GPS" :          ( "R44  0",         ["  ", ","]        ),
        "Seapath-Gyro" :     ( "R104  3",        ["  ", ","]        ),
        "PRDID-Gyro" :       ( "R132  4",        ["  ", ","]        ),
        "HPR410-HiPAP" :     ( "R496  10",       ["  ", ","]        ),
        "USBL" :             ( "P  D   3",       ["   ", "  "]      ),
        "Digiquartz-Depth" : ( "D     3  19  1", ["   ", "  ", " "] ),
    }

    FormatData(path, outputDirectory, entries)

if __name__ == "__main__":
    Main()