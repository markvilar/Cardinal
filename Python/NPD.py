import datetime

from typing import List

from utilities import custom_split

class Line:
    def __init__(self, data: str):
        self._data = data.replace("\n", "")

    def __repr__(self):
        return self._data
    
    def __str__(self):
        return self._data
    
    def get_data(self):
        return self._data
    
    def get_data_count(self, delimiter: str = "  "):
        return len(self._data.split(delimiter))

    def has_id(self, id: str):
        return self.starts_with(id)

    def starts_with(self, prefix: str):
        return self._data.startswith(prefix)

    def remove_prefix(self, prefix: str):
        if self._data.startswith(prefix):
            return self._data[len(prefix):]
        return self._data

class Entry:
    def __init__(self, id: str, data_separators: List[str], line: Line):
        # Remove ID and following whitespaces.
        line = line.remove_prefix(id + "  ")

        # Separate time and data entry.
        splits = custom_split(line, data_separators)
        time = splits[0]
        data = splits[1:]

        self._id = id
        self._time = time
        self._data = list(filter(None, data))

    def __repr__(self):
        return self._id + ": " + self._time + "," + " ".join(self._data)
    
    def __str__(self):
        return self._id + ": " + self._time + "," + " ".join(self._data)

    def get_time(self):
        return self._time

    def get_data(self):
        return self._data

class Timestamp:
    def __init__(self, time: str, appendage: str = "000"):
        self._time = time + appendage

    def get_time(self):
        return self._time

    def get_epoch(self):
        return datetime.datetime.timestamp( \
            datetime.datetime.strptime(self._time, \
            "%Y:%m:%d:%H:%M:%S.%f"))