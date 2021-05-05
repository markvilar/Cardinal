from typing import Dict, Tuple

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import msgpack
import numpy as np
import pandas as pd
import quaternion 

import utilities
import georeferencing

def extract_data(slam_data: Dict, navigation_data: Dict, reference: bool, \
    show_figures: bool):
    """
    Georeferences SLAM output in the UTM datum.
    """
    # Select APS and gyroscope segment for keyframe trajectory.
    keyframe_start = slam_data["Keyframes"]["TimestampSynced"].iat[0]
    keyframe_end = slam_data["Keyframes"]["TimestampSynced"].iat[-1]

    aps_start = utilities.closest_point(keyframe_start, \
        navigation_data["APS"]["Epoch"])
    aps_end = utilities.closest_point(keyframe_end, \
        navigation_data["APS"]["Epoch"]) + 1

    gyroscope_start = utilities.closest_point(keyframe_start, \
        navigation_data["Gyroscope"]["Epoch"])
    gyroscope_end = utilities.closest_point(keyframe_end, \
        navigation_data["Gyroscope"]["Epoch"]) + 1

    # Create data container.
    data = {}
    data["Camera"] = slam_data["Keyframes"]
    data["APS"]= navigation_data["APS"].iloc[aps_start:aps_end]
    data["Gyroscope"]= navigation_data["Gyroscope"] \
        .iloc[gyroscope_start:gyroscope_end]

    if reference:
        georeferencing.slam_relative_georeferencing(data)
    else:
        georeferencing.aps_relative_georeferencing(data)

    if show_figures:
        plt.show()
        
def main():
    slam_directory = "/home/martin/dev/Cardinal/Data/SLAM-CLAHE/"
    navigation_directory = "/home/martin/dev/Cardinal/Data/Filtered/Dive-1/"

    show_figures = True
    reference = False

    paths = {}
    paths["Frames"] = slam_directory + "Frame-Trajectory.csv"
    paths["Keyframes"] = slam_directory + "Keyframe-Trajectory.csv"
    paths["Map"] = slam_directory + "Map.msg"
    paths["APS"] = navigation_directory + "ROV-APS.csv"
    paths["Gyroscope"] = navigation_directory + "ROV-Gyroscope.csv"

    slam_data = {}
    slam_data["Frames"] = pd.read_csv(paths["Frames"])
    slam_data["Keyframes"] = pd.read_csv(paths["Keyframes"])

    navigation_data = {}
    navigation_data["APS"] = pd.read_csv(paths["APS"])
    navigation_data["Gyroscope"] = pd.read_csv(paths["Gyroscope"])

    extract_data(slam_data, navigation_data, reference, show_figures)

if __name__ == "__main__":
    main()
