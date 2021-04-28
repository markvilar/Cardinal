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

def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Parameters
    ----------
        ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

def closest_point(reference, data):
    relative = data - reference
    return np.argmin(np.abs(relative))

def quaternion_from_axis_angle(axis: np.ndarray, angle: float):
    assert axis.shape == (3,), "The axis vector must be (3,)."
    assert np.linalg.norm(axis) == 1.0, "The axis vector must have norm 1."
    imaginary = np.sin(angle/2) * axis
    real = np.cos(angle/2)
    return quaternion.quaternion(real, imaginary[0], imaginary[1], imaginary[2])

def vector_to_quaternion(vectors: np.ndarray):
    n = vectors.shape[0]
    quats = np.zeros(( n, 4 ), dtype=float)
    quats[:, 1:4] = vectors
    return quaternion.as_quat_array(quats)

def quaternion_to_vector(quats: np.ndarray):
    quats = quaternion.as_float_array(quats)
    vectors = quats[:, 1:4]
    return vectors
