from dataclasses import dataclass

import pandas as pd

from tqdm import tqdm

from eiva import EivaRecord
from file_utils import FileReader

def main():
    """
    arguments:
        file_path   - string
        output      - string
        instruments - [name, identifier, sentence]
    """

    # 20150625 - Tautra, 20150626 - Tautra, 20161207 - Tautra
    root_dir = "/home/martin/pCloudDrive/research/data/20161207-tautra/raw/navigation"
    output_dir = "/home/martin/pCloudDrive/research/data/20161207-tautra"
    file_name = "20161207_110848_G.NPD"
    file_path =  root_dir + '/' + file_name

    reader = FileReader(file_path, skip_header=False)

    # Construct record instruments
    date = "20161207"
    time = "110848"
    record_name = date + "-" + time
    record = EivaRecord(name=record_name)
    record.add_instrument("vessel_gps",   "R44",   "$GPGGA")
    record.add_instrument("vessel_mru",  "R104",   "$GPHDT")
    record.add_instrument("rov_aps",     "R496", "$PSIMSSB")
    record.add_instrument("rov_gyro",    "R132",   "$PRDID")

    # Skip header
    while not reader.is_end_of_file():
        line = reader.read_line()
        if line.strip() == "/H0":
            break

    num_entries = reader.lines_total() - reader.line_count()
    for i in tqdm(range(num_entries), desc="Reading..."):
        record.process_entry(reader.read_line())
        
    record.save(output_dir)

if __name__ == '__main__':
    main()
