import csv

def FormatRawROVData(inputPath: str, outputPath: str):
    with open(inputPath, 'r') as inputFile, open(outputPath, 'w', newline='') as outputFile:
        data = {}
        writer = csv.writer(outputFile)
        
        header = inputFile.readline()
        printLine = True

        while True:
            line = inputFile.readline()

            if line == '':
                break
            else:
                line = line.replace("\n", "")
                entries = line.split("\t")
                entries[1:] = [float(entry) for entry in entries[1:]]
                writer.writerow(entries)

def main():
    inputPath = "./Data/20210122--0959raw_data.log"
    outputPath = "./Data/20210122--0959.csv"
    FormatRawROVData(inputPath, outputPath)

if __name__ == "__main__":
    main()