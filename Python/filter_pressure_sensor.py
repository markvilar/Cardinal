import argparse
import datetime
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/scientific.mplstyle")

from typing import Dict, List

import data
import filters
import utilities
import utm

def filter_pressure_sensor(data_config: data.DataConfiguration, \
    filter_config: filters.FilterConfiguration, time_limits: List, \
    depth_limits: List):
    """
    """
    data = pd.read_csv(data_config.input)

    # Extract relevant data for filtering.
    time = data["Epoch"].to_numpy()
    depth = data["Depth"].to_numpy()
    filter_config.sample_frequency = 1 / np.mean(time[1:] - time[0:-1])

    # --------------------------------------------------------------------------
    # ---- Filtering. ----------------------------------------------------------
    # --------------------------------------------------------------------------

    # Add end values.
    filtered_depth = filters.add_appendage(depth.copy(), filter_config)

    # Filter data and account for time delay.
    filtered_depth, filter_delay = filters.FIR_filter(filtered_depth, \
        filter_config)

    filtered_time = time - filter_delay

    print("\nPressure Sensor:")
    print(" - Sampling time:      {0:.4f}".format( \
        1 / filter_config.sample_frequency))
    print(" - Sampling frequency: {0:.4f}".format( \
        filter_config.sample_frequency))
    print(" - Filter time delay:  {0:.4f}".format(filter_delay))

    # Remove end values.
    filtered_depth = filters.remove_appendage(filtered_depth, filter_config)

    filtered_data = pd.DataFrame()
    filtered_data["Epoch"] = filtered_time
    filtered_data["Depth"] = filtered_depth

    # --------------------------------------------------------------------------
    # ---- Datetime calculations. ----------------------------------------------
    # --------------------------------------------------------------------------

    times = []
    for epoch in filtered_data["Epoch"]:
        time = datetime.datetime.fromtimestamp(epoch).strftime( \
		    data_config.datetime_format)
        times.append(time)

    filtered_data["Datetime"] = np.array(times, dtype=str)

    # --------------------------------------------------------------------------
    # ---- Plotting. -----------------------------------------------------------
    # --------------------------------------------------------------------------
    
    # depth plot.
    fig1, ax1 = plt.subplots(figsize=(4, 4))
    ax1.plot(data["Epoch"] - data["Epoch"][0], data["Depth"], \
        linewidth=1.0, label="Unfiltered")
    ax1.plot(filtered_data["Epoch"] - data["Epoch"][0], \
	    filtered_data["Depth"], linewidth=1.0, label="Filtered")
    ax1.set_xlim(time_limits)
    ax1.set_ylim(depth_limits)
    ax1.set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax1.set_ylabel(r"Depth, $D$ $[\text{m}]$")
    ax1.legend()

    if data_config.show_figures:
        plt.show()

    # --------------------------------------------------------------------------
    # ---- Save data. ----------------------------------------------------------
    # --------------------------------------------------------------------------

    if data_config.save_figures:
        fig1.savefig(data_config.output + "ROV-Pressure-Sensor-Depth.eps", 
            dpi=300)

    if data_config.save_output:
        filtered_data = pd.DataFrame(filtered_data)
        filtered_data.to_csv(data_config.output + "ROV-Pressure-Sensor.csv", 
            sep=',')

def main():
    # Plot limits.
    time_limits = [450, 480]
    depth_limits = [55, 59]

    # Parse arguments.
    parser = argparse.ArgumentParser( \
        description="Filter HiPAP data with a FIR filter.")
    parser.add_argument("input", type=str, help="Input file path.")
    parser.add_argument("output", type=str, help="Output directory path.")
    parser.add_argument("order", type=int, help="Filter order.")
    parser.add_argument("cutoff", type=float, help="Filter cutoff.")
    parser.add_argument("appendage", type=int, help="Filter appendage.")
    parser.add_argument('--show_figures', type=bool, default=False, \
        help= "Show figures.", action=argparse.BooleanOptionalAction)
    parser.add_argument('--save_figures', type=bool, default=False, \
        help= "Save figures.", action=argparse.BooleanOptionalAction)
    parser.add_argument('--save_output', type=bool, default=False, \
        help= "Save output.", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    # Data configuration.
    data_config = data.DataConfiguration(args.input, args.output, \
        args.show_figures, args.save_figures, args.save_output)

    # Filter configuration.
    filter_config = filters.FilterConfiguration(args.order, args.cutoff, \
        args.appendage)
    
    # Filter data.
    filter_pressure_sensor(data_config, filter_config, time_limits, \
        depth_limits)

if __name__ == '__main__':
    main()
