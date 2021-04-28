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

def calculate_lever_arm(arm: np.ndarray, angle: float):
    """
    Calculates the lever arm of the camera in the camera coordinate system.

    Parameters
    ----------
    arm: Lever arm expressed in the ROV coordinate system.
    angle : Rotation of the camera relative to the ROV coordinate system.

    Return
    ------
    array: Lever arm in camera coordinate system.
    """
    a = arm[1]
    b = arm[2]
    c = np.sqrt(a*a + b*b)
    alpha = np.arccos(b / c)
    phi = angle - alpha
    d = c * np.cos(phi)
    e = c * np.sin(phi)

    x = -arm[0]
    y = e
    z = -d
    return np.array([ x, y, z ])

def plot_3D_trajectory(trajectory: np.array, figsize: Tuple=(6, 6), \
    label: str="", xlabel: str="", ylabel: str="", zlabel: str="", \
    title: str="", legend: bool=False, equal_axes: bool=False):
    """
    Parameters
    ----------
    trajectory: (N, 3), the trajectory
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], label=label)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.set_title(title)
    if equal_axes:
        utilities.set_axes_equal(ax)

    return (fig, ax)

def calculate_transducer_trajectory(positions: np.ndarray, \
    attitudes: np.ndarray, lever_arm: np.ndarray):
    """
    Calculates the local transducer trajectory from the camera positions,
    attitudes, and relative lever arm.

    Parameters
    ----------
    positions: (N, 3), camera positions in the object CS.
    attitudes: (N, 4), camera attitudes in the object CS.
    lever_arm: (N, 3), Lever arm from camera to transducer in the camera CS.

    Returns
    -------
    np.array: The transducer trajectory.
    """
    # Set up camera direction vectors.
    directions = np.zeros(positions.shape, dtype=float)
    directions[:, -1] = 1.0

    # Convert lever arm, position and attitude to quaternions.
    lever_arm = utilities.vector_to_quaternion(lever_arm)
    directions = utilities.vector_to_quaternion(directions)
    attitudes = quaternion.as_quat_array(attitudes)

    # Calculate camera directions.
    rotated_directions = attitudes * directions * attitudes.conjugate()
    rotated_directions = utilities.quaternion_to_vector(rotated_directions)

    # Calculate trajectory of transducer with SLAM trajectory and lever arm.
    rotated_lever_arms = attitudes * lever_arm * attitudes.conjugate()
    rotated_lever_arms = utilities.quaternion_to_vector(rotated_lever_arms)
    transducer_positions = positions + rotated_lever_arms

    # Plot camera trajectory.
    fig, ax = plot_3D_trajectory(positions, xlabel=r"X $[\text{m}]$", \
        ylabel=r"Y $[\text{m}]$", zlabel=r"Z $[\text{m}]$", \
        title=r"SLAM Trajectory", label="Camera", equal_axes=True)

    # Plot camera directions.
    ax.quiver(positions[:, 0], positions[:, 1], positions[:, 2], \
        rotated_directions[:, 0], rotated_directions[:, 1], 
        rotated_directions[:, 2], length=0.3)

    # Plot transducer trajectory.
    ax.plot(transducer_positions[:, 0], transducer_positions[:, 1], \
        transducer_positions[:, 2], label="Transducer")

    ax.legend()

    return transducer_positions

def calculate_levelled_trajectory(positions: np.ndarray, \
    attitudes: np.ndarray, lever_arms: np.ndarray, \
    transducer_positions: np.ndarray, inclination: float):
    """
    Calculates the levelled trajectories, accounting for the camera 
    inclination.

    Parameters
    ----------
    positions:            (N, 3) - Camera positions in the object CS.
    attitudes:            (N, 4) - Camera attitudes in the object CS.
    transducer_positions: (N, 3) - Transducer positions in the object CS.
    lever_arms:           (N, 3) - Lever arms in the camera CS.
    inclination:                 - The camera inclination angle.

    Returns
    -------
    np.array: The transducer trajectory.
    """
    # Calculate quaternion for inclination rotation.
    inclination_axis = np.array([ 1.0, 0.0, 0.0 ], dtype=float)
    inclination = utilities.quaternion_from_axis_angle(inclination_axis, \
        -inclination)

    # Create direction vectors for the camera positions.
    directions = np.zeros(positions.shape, dtype=float)
    directions[:, -1] = 1.0

    # Convert to quaternions.
    positions = utilities.vector_to_quaternion(positions)
    attitudes = quaternion.as_quat_array(attitudes)
    directions = utilities.vector_to_quaternion(directions)
    transducer_positions = utilities.vector_to_quaternion(transducer_positions)
    lever_arms = utilities.vector_to_quaternion(lever_arms)

    # Positions are rotated with the object CS.
    positions = inclination * positions * inclination.conjugate()
    attitudes = inclination * attitudes * inclination.conjugate()
    transducer_positions = inclination * transducer_positions \
        * inclination.conjugate()

    # Calculate new attitudes and directions.
    attitudes = inclination * attitudes
    directions = attitudes * directions * attitudes.conjugate()
    
    # Convert back to vectors.
    positions = utilities.quaternion_to_vector(positions)
    attitudes = quaternion.as_float_array(attitudes)
    directions = utilities.quaternion_to_vector(directions)
    transducer_positions = utilities.quaternion_to_vector(transducer_positions)

    # Plot rotated keyframe positions.
    fig, ax = plot_3D_trajectory(positions, xlabel=r"X $[\text{m}]$", \
        ylabel=r"Y $[\text{m}]$", zlabel=r"Z $[\text{m}]$", \
        title=r"Levelled Trajectory", label="Camera", equal_axes=True)

    # Plot rotated direction vectors.
    ax.quiver(positions[:, 0], positions[:, 1], positions[:, 2], \
        directions[:, 0], directions[:, 1], directions[:, 2], length=0.3)

    # Plot rotated transducer positions.
    ax.plot(transducer_positions[:, 0], transducer_positions[:, 1], \
        transducer_positions[:, 2], label="Transducer")

    ax.legend()

    return positions, attitudes, transducer_positions

def calculate_georeferenced_trajectory(pitch, yaw, roll):
    """
    Calculates the levelled trajectories, accounting for the camera 
    inclination.

    Parameters
    ----------
    positions: (N, 3), camera positions in the object CS.
    attitudes: (N, 4), camera attitudes in the object CS.
    directions: (N, 3), camera view directions in the camera CS.
    lever_arm: (N, 3), Lever arm from camera to transducer in the camera CS.

    Returns
    -------
    np.array: The transducer trajectory.
    """
    roll_axis = np.array([ 0.0, 1.0, 0.0 ], dtype=float)
    pitch_axis = np.array([ 1.0, 0.0, 0.0 ], dtype=float)
    yaw_axis = np.array([ 0.0, 0.0, 1.0], dtype=float)

    roll_quat = utilities.quaternion_from_axis_angle(roll_axis, roll)
    pitch_quat = utilities.quaternion_from_axis_angle(pitch_axis, pitch)
    yaw_quat = utilities.quaternion_from_axis_angle(yaw_axis, heading)
    raise NotImplementedError

def georeference_keyframe_data(data: Dict):
    # Set up sensor configuration.
    measured_distances = np.array([ 0.21, 1.40, 2.00 ])
    measured_inclination = 48 * np.pi / 180
    lever_arm = calculate_lever_arm(measured_distances, measured_inclination)
    inclination = measured_inclination

    # Inclination and lever arm printout.
    print("Measured distances:   {0}, {1}".format( measured_distances, \
        np.linalg.norm(measured_distances) ))
    print("Measured inclination: {0}, {1}".format( measured_inclination, \
        measured_inclination* 180 / np.pi))
    print("Calculated lever arm: {0}, {1}".format( lever_arm, \
        np.linalg.norm(lever_arm) ))

    # Extract data.
    aps_positions = np.stack([ data["APS"]["UTM Easting"], \
        data["APS"]["UTM Northing"], -data["APS"]["Depth"] ]).T
    positions = np.stack([ \
        data["Keyframes"]["PositionX"], \
        data["Keyframes"]["PositionY"], \
        data["Keyframes"]["PositionZ"] ]).T
    attitudes = np.stack([ \
        data["Keyframes"]["Quaternion1"], \
        data["Keyframes"]["Quaternion2"], \
        data["Keyframes"]["Quaternion3"], \
        data["Keyframes"]["Quaternion4"] ]).T

    roll = data["Gyroscope"]["Roll"].iloc[0]
    pitch = data["Gyroscope"]["Pitch"].iloc[0]
    heading = data["Gyroscope"]["Heading"].iloc[0]

    # Allocate lever arm array.
    lever_arms = np.tile(lever_arm, ( positions.shape[0], 1 ))

    # Visualize the APS trajectory.
    fig1, ax1 = plot_3D_trajectory(aps_positions, title="APS Trajectory", \
        equal_axes=True)

    # Calculate transducer positions in object coordinate system.
    transducer_positions = calculate_transducer_trajectory(positions, \
        attitudes, lever_arms)

    # Calculate levelled trajectory.
    positions, attitudes, transducer_positions = \
        calculate_levelled_trajectory(positions, attitudes, lever_arms, \
        transducer_positions, inclination)

    # Plot positions to debug.
    #fig2, ax2 = plot_3D_trajectory(positions, title="Debug", equal_axes=True)

    # Calculate georeferenced trajectory.
    #calculate_georeferenced_trajectory(positions, attitudes, )

    plt.show()

def georeference_slam_data(slam_data: Dict, navigation_data: Dict, \
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
    keyframe_data = {}
    keyframe_data["Keyframes"] = slam_data["Keyframes"]
    keyframe_data["APS"]= navigation_data["APS"].iloc[aps_start:aps_end]
    keyframe_data["Gyroscope"]= navigation_data["Gyroscope"] \
        .iloc[gyroscope_start:gyroscope_end]

    # Georeference keyframe trajectory.
    georeference_keyframe_data(keyframe_data)

    if show_figures:
        plt.show()
        
def main():
    slam_directory = "/home/martin/dev/Cardinal/Data/SLAM-CLAHE/"
    navigation_directory = "/home/martin/dev/Cardinal/Data/Filtered/Dive-1/"

    show_figures = True

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

    georeference_slam_data(slam_data, navigation_data, show_figures)

if __name__ == "__main__":
    main()
