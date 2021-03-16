import datetime

from typing import List

from Utilities import CustomSplit

class Line:
    def __init__(self, data: str):
        self._data = data.replace("\n", "")

    def __repr__(self):
        return self._data
    
    def __str__(self):
        return self._data
    
    def GetData(self):
        return self._data
    
    def GetDataCount(self, delimiter: str = "  "):
        return len(self._data.split(delimiter))

    def HasID(self, id: str):
        return self.StartsWith(id)

    def StartsWith(self, prefix: str):
        return self._data.startswith(prefix)

    def RemovePrefix(self, prefix: str):
        if self._data.startswith(prefix):
            return self._data[len(prefix):]
        return self._data

class Entry:
    def __init__(self, id: str, dataSeparators: List[str], line: Line):
        # Remove ID and following whitespaces.
        line = line.RemovePrefix(id + "  ")

        # Separate time and data entry.
        splits = CustomSplit(line, dataSeparators)
        time = splits[0]
        data = splits[1:]

        self._id = id
        self._time = time
        self._data = list(filter(None, data))

    def __repr__(self):
        return self._id + ": " + self._time + "," + " ".join(self._data)
    
    def __str__(self):
        return self._id + ": " + self._time + "," + " ".join(self._data)

    def GetTime(self):
        return self._time

    def GetData(self):
        return self._data

class Timestamp:
    def __init__(self, time: str, appendage: str = "000"):
        self._time = time + appendage

    def GetTime(self):
        return self._time

    def GetEpoch(self):
        return datetime.datetime.timestamp( \
            datetime.datetime.strptime(self._time, \
            "%Y:%m:%d:%H:%M:%S.%f"))