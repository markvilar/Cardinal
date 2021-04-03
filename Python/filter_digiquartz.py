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
    plot_start = 1611313500
    plot_stop = 1611313550

    # Load data.
    input_paths = {
        "ROV-Digiquartz" : "./Data/Outlier-Filtered/ROV-Dive-2/ROV-Digiquartz.csv"
    }
    data = utilities.load_csv_files(input_paths)
    data = data["ROV-Digiquartz"]

    # Extract relevant data for filtering.
    time = data["Epoch"].to_numpy()
    depth = data["Depth"].to_numpy()

    # Calculate sampling frequency.
    sample_frequency = 1 / np.mean(time[1:] - time[0:-1])

    # --------------------------------------------------------------------------
    # ---- Filtering. ----------------------------------------------------------
    # --------------------------------------------------------------------------

    # Filter parameters.
    filter_order = 5
    filter_cutoff = 0.25
    filter_boundary = 10

    # Add end values.
    filtered_depth = filters.add_boundary_values(depth, filter_boundary)

    # Filter data and account for time delay.
    filtered_depth, delay = filters.FIR_filter(filtered_depth, \
        sample_frequency, filter_order, filter_cutoff, axis=1)

    filtered_time = time - delay

    print("Sampling time: {0}".format(1/sample_frequency))
    print("Filter time delay: {0}".format(delay))

    # Remove end values.
    filtered_depth = filters.remove_boundary_values(filtered_depth, \
        filter_boundary)

    filtered_data = pd.DataFrame()
    filtered_data["Epoch"] = filtered_time
    filtered_data["Depth"] = filtered_depth

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
    
    # depth plot.
    fig1, ax1 = plt.subplots(figsize=(14, 7))
    ax1.plot(data["Epoch"], data["Depth"], \
        linewidth=1, label="Unfiltered")
    ax1.plot(filtered_data["Epoch"], filtered_data["Depth"], \
        linewidth=1, label="Filtered")
    ax1.set_xlim([plot_start, plot_stop])
    ax1.set_ylim([55, 60])
    ax1.set_title("Depth")
    ax1.legend()

    if show_figures:
        plt.show()

    # --------------------------------------------------------------------------
    # ---- Save data. ----------------------------------------------------------
    # --------------------------------------------------------------------------

    if save_figures:
        fig1.savefig(figure_directory + "ROV-Digiquartz-Depth.png", dpi=300)

    if save_csv:
        filtered_data = pd.DataFrame(filtered_data)
        filtered_data.to_csv(output_directory + "ROV-Digiquartz.csv", sep=',')

if __name__ == '__main__':
    main()