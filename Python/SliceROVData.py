import csv
import datetime

def SliceROVData(inputPath: str, outputPath: str, startTime: str, endTime: str):
    with open(inputPath, 'r') as inputFile, open(outputPath, 'w', newline='') as outputFile:

        reader = csv.reader(inputFile, delimiter=',')
        writer = csv.writer(outputFile, delimiter=',')

        startTime = datetime.datetime.strptime(startTime, "%H:%M:%S")
        endTime = datetime.datetime.strptime(endTime, "%H:%M:%S")

        print(startTime)
        print(endTime)

        for row in reader:
            if row:
                time = datetime.datetime.strptime(row[0], "%H:%M:%S.%f")
                if startTime < time and time < endTime:
                    writer.writerow(row)

def main():
    inputPath = "./Data/20210122--0959.csv"
    outputPath = "./Data/20210122--0959-sliced.csv"
    startTime = "11:59:15"
    endTime = "13:15:38"
    SliceROVData(inputPath, outputPath, startTime, endTime)

if __name__ == "__main__":
    main()