from enum import Enum
from typing import Dict, List, Tuple

import pandas as pd

class NmeaSentenceType(Enum):
    GPGGA = 1
    GPHDT = 2
    GPZDA = 3
    PRDID = 4
    PSIMSSB = 5

def nmea_sentence_type(type: str) -> NmeaSentenceType:
    return

def parse_nmea_sentence(line: str) -> pd.Series:
    """
    Parse a NMEA sentence.
    """
    sentence_type = line.split(",")[0]
    if sentence_type == "$GPGGA":
        return parse_gpgga(line)
    elif sentence_type == "$GPHDT":
        return parse_gphdt(line)
    elif sentence_type == "$GPZDA":
        return parse_gpzda(line)
    elif sentence_type == "$PRDID":
        return parse_prdid(line)
    elif sentence_type == "$PSIMSSB":
        return parse_psimssb(line)
    else:
        return pd.Series()

def parse_gpzda(line: str) -> pd.Series:
    """ 
    Parse a NMEA line as a GPZDA message - UTC time and date.
    """
    entries = line.split(',')

    assert len(entries) == 7, "GPZDA: Invalid number of entries"

    data = {}
    data["utc"] = entries[1]
    data["day"]= entries[2]
    data["month"] = entries[3]
    data["year"] = entries[4]
    data["offset"] = entries[5]
    data["checksum"] = entries[6]
    return pd.Series(data)

def parse_gpgga(line: str) -> pd.Series:
    """ 
    Parse a NMEA line as a GPGGA message - Global positioning system.
    """
    entries = line.split(',')

    assert len(entries) == 15, "GPGGA: Invalid number of entries"

    data = {}
    data["utc"] = entries[1]
    data["latitude"] = entries[2]
    data["latitude_dir"] = entries[3]
    data["longitude"] = entries[4]
    data["longitude_dir"] = entries[5]
    data["undulation"] = entries[11]
    data["undulation_unit"] = entries[12]
    return pd.Series(data)

def parse_gphdt(line: str) -> pd.Series:
    """ 
    Parse a NMEA line as a GPHDT message - Heading.
    """
    entries = line.split(',')

    assert len(entries) == 3, "GPHDT: Invalid number of entries"

    data = {}
    data["heading"] = entries[1]
    return pd.Series(data)

def parse_prdid(line: str) -> pd.Series:
    """ 
    Parse a NMEA line as a PRDID message - Heading.
    """
    entries = line.split(',')

    assert len(entries) == 5, "PRDID: Invalid number of entries"

    data = {}
    data["pitch"] = entries[1]
    data["roll"]= entries[2]
    data["heading"] = entries[3]
    return pd.Series(data)

def parse_psimssb(line: str) -> pd.Series:
    """ 
    Parse a NMEA line as a PSIMSSB message - Short baseline position.
    Message defined by the Kongsberg NMEA extension.
    """
    entries = line.split(',')
    assert len(entries) == 15, "PSIMSSB: Invalid number of entries"

    data = {}

    data["utc"] = entries[1]
    data["code"] = entries[2]
    data["status"] = entries[3]
    data["error"] = entries[4]
    data["coordinate_system"] = entries[5]
    data["orientation"] = entries[6]
    data["filter"] = entries[7]
    data["x"] = entries[8]
    data["y"] = entries[9]
    data["depth"] = entries[10]
    data["accuracy"] = entries[11]
    return pd.Series(data)
