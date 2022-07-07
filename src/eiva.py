from datetime import datetime
from dataclasses import dataclass, field

import pandas as pd

from geodesic import latlon_to_utm
from nmea import parse_nmea_sentence

@dataclass
class EivaInstrument:
    name: str = ""
    identifier: str = ""
    sentence: str = ""

@dataclass
class EivaRecord:
    name: str = ""
    instruments: list[EivaInstrument] = field(default_factory=list)
    data_frames: dict[str, pd.DataFrame] = field(default_factory=dict)

    def add_instrument(self, name: str, identifier: str, sentence: str):
        """ """
        self.instruments.append(EivaInstrument(name, identifier, sentence))

    def process_entry(self, entry):
        """ """
        if entry[0] == "R":
            id, num, time, msg = entry.split()
            date = datetime.strptime(time, "%Y:%m:%d:%H:%M:%S.%f")
            timestamp = datetime.timestamp(date)
            date_string = date.strftime("%Y-%m-%d_%H-%M-%S.%f")

            data = pd.Series()
            data["timestamp"] = timestamp
            data["datetime"] = date_string
            data = parse_nmea_sentence(msg)

            for instrument in self.instruments:
                if id == instrument.identifier:
                    self.add_series(instrument.name, data)

    def add_series(self, name, series):
        """ """
        if name in self.data_frames:
            self.data_frames[name] \
                = pd.concat([self.data_frames[name], series.to_frame().T])
        else:
            self.data_frames[name] = series.to_frame().T

    def save(self, root_path):
        for label, data_frame in self.data_frames.items():
            """ """
            path = root_path + "/" + self.name + "_" + label + ".csv"
            data_frame.to_csv(path, index=False)
