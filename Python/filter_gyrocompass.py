import datetime
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from mpl_toolkits.mplot3d import Axes3D
from typing import Dict

import filters
import utilities
import utm

def main():
    # Script variables.
    save_figures = True
    show_figures = False
    save_csv = True
    figure_directory = "./Figures/Dive-2-Filtered/"
    output_directory = "./Output/Dive-2-Filtered/"
    plot_start = 1611313450
    plot_stop = 1611313550

    # Load data.
    input_paths = {
        "ROV-Gyrocompass" : "./Data/Outlier-Filtered/ROV-Dive-2/ROV-Gyrocompass.csv"
    }
    data = utilities.load_csv_files(input_paths)
    data = data["ROV-Gyrocompass"]

    # Extract relevant data for filtering.
    time = data["Epoch"].to_numpy()
    roll = data["Roll"].to_numpy()
    pitch = data["Pitch"].to_numpy()
    heading = data["Heading"].to_numpy()

    # Unclamp heading and calculate sampling frequency.
    heading = utilities.unclamp_signal(heading, 0, 360, 0.9)
    sample_frequency = 1 / np.mean(time[1:] - time[0:-1])

    # --------------------------------------------------------------------------
    # ---- Filtering. ----------------------------------------------------------
    # --------------------------------------------------------------------------

    # Filter parameters.
    filter_order = 6
    filter_cutoff = 0.1
    filter_boundary = 10

    # Add end values.
    signals = np.stack((roll, pitch, heading))
    signals = filters.add_boundary_values(signals, filter_boundary)

    # Filter data and account for time delay.
    filtered_signals, delay = filters.FIR_filter(signals, \
        sample_frequency, filter_order, filter_cutoff, axis=1)

    filtered_time = time - delay

    print("Sampling time: {0}".format(1/sample_frequency))
    print("Filter time delay: {0}".format(delay))

    # Remove end values.
    filtered_signals = filters.remove_boundary_values(filtered_signals, \
        filter_boundary)

    # Clamp heading.
    filtered_signals[2] = utilities.clamp_signal(filtered_signals[2], 0, 360)

    filtered_data = pd.DataFrame()
    filtered_data["Epoch"] = filtered_time
    filtered_data["Roll"] = filtered_signals[0]
    filtered_data["Pitch"] = filtered_signals[1]
    filtered_data["Heading"] = filtered_signals[2]

    # --------------------------------------------------------------------------
    # ---- Datetime calculations. ----------------------------------------------
    # --------------------------------------------------------------------------

    times = []
    for epoch in filtered_data["Epoch"]:
        time = datetime.datetime.fromtimestamp(epoch).strftime("%Y:%m:%d:%H:%M:%S.%f")
        times.append(time)

    filtered_data["Datetime"] = np.array(times, dtype=str)

    # --------------------------------------------------------------------------
    # ---- Plotting. -----------------------------------------------------------
    # --------------------------------------------------------------------------
    
    # Roll plot.
    fig1, ax1 = plt.subplots(figsize=(14, 7))
    ax1.plot(data["Epoch"], data["Roll"], \
        linewidth=1, label="Unfiltered")
    ax1.plot(filtered_data["Epoch"], filtered_data["Roll"], \
        linewidth=1, label="Filtered")
    ax1.set_xlim([plot_start, plot_stop])
    ax1.set_title("Roll")
    ax1.legend()

    # Pitch plot.
    fig2, ax2 = plt.subplots(figsize=(14, 7))
    ax2.plot(data["Epoch"], data["Pitch"], \
        linewidth=1, label="Unfiltered")
    ax2.plot(filtered_data["Epoch"], filtered_data["Pitch"], \
        linewidth=1, label="Filtered")
    ax2.set_xlim([plot_start, plot_stop])
    ax2.set_title("Pitch")
    ax2.legend()

    # Heading plot.
    fig3, ax3 = plt.subplots(figsize=(14, 7))
    ax3.plot(data["Epoch"], data["Heading"], \
        linewidth=1, label="Unfiltered")
    ax3.plot(filtered_data["Epoch"], filtered_data["Heading"], \
        linewidth=1, label="Filtered")
    ax3.set_xlim([plot_start, plot_stop])
    ax3.set_title("Heading")
    ax3.legend()

    if show_figures:
        plt.show()

    # --------------------------------------------------------------------------
    # ---- Save data. ----------------------------------------------------------
    # --------------------------------------------------------------------------

    if save_figures:
        fig1.savefig(figure_directory + "ROV-Gyrocompass-Roll.png", dpi=300)
        fig2.savefig(figure_directory + "ROV-Gyrocompass-Pitch.png", dpi=300)
        fig3.savefig(figure_directory + "ROV-Gyrocompass-Heading.png", dpi=300)

    if save_csv:
        filtered_data = pd.DataFrame(filtered_data)
        filtered_data.to_csv(output_directory + "ROV-Gyrocompass.csv", sep=',')

if __name__ == '__main__':
    main()