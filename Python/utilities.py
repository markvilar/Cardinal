import csv
import re
import sys

import numpy as np
import pandas as pd
import quaternion 

from typing import Dict, List

def load_csv_files(file_paths: Dict) -> Dict:
    # Dict of dicts.
    data = {}
    for name, path in file_paths.items():
        data[name] = pd.read_csv(path)
    return data

def write_csv_file(path: str, data: Dict):
    with open(path, 'w', newline='') as file:
        keys = list(data.keys())
        values = list(data.values())

        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        
        for index in range(len(values[0])):
            row = [value[index] for value in values]
            writer.writerow(dict(zip(keys, row)))

def unclamp_signal(data: np.ndarray, min_value: float, max_value: float, \
    threshold: float=0.95):
    differences = np.insert(data[1:] - data[:-1], 0, 0.0)
    steps = np.zeros(differences.shape, dtype=int)
    steps[differences > threshold * (max_value - min_value)] = -1
    steps[differences < -threshold * (max_value - min_value)] = 1
    revolutions = np.cumsum(steps)
    return data + revolutions * (max_value - min_value)

def clamp_signal(data: np.ndarray, min_value: float, max_value: float):
    upper_mask = data > max_value
    lower_mask = data < min_value
    adjustments = np.zeros(data.shape, dtype=float)
    adjustments[upper_mask] = np.ceil(data[upper_mask] \
        / (max_value - min_value)) * (max_value - min_value)
    adjustments[lower_mask] = -np.floor(data[lower_mask] \
        / (max_value - min_value)) * (max_value - min_value)
    return data + adjustments

def convert_dictionary_values_numpy(data: Dict, data_types: Dict):
    for key in data:
        data[key] = np.array(data[key], dtype=data_types[key])
    return data

def progress_bar(percentage_done: int, bar_width: int=60):
	progress = int(bar_width * percentage_done / 100)
	bar = '=' * progress + ' ' * (bar_width - progress)
	sys.stdout.write('[{0}] {1:.2f}{2}\r'.format(bar, percentage_done, '%'))
	sys.stdout.flush()

def custom_split(string, separator_list):
    # Create regular expression dynamically.
    regular_expression = '|'.join(map(re.escape, separator_list))
    return re.split(regular_expression, string)

def closest_point(reference, data):
    relative = data - reference
    return np.argmin(np.abs(relative))
