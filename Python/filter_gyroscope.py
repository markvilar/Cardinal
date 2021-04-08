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

def filter_gyroscope(data_config: data.DataConfiguration, 
    filter_config: filters.FilterConfiguration, \
    time_limits: List, roll_limits: List, pitch_limits: List, \
    heading_limits: List):
    """
    """
    data = pd.read_csv(data_config.input)

    # Extract relevant data for filtering.
    time = data["Epoch"].to_numpy()
    roll = data["Roll"].to_numpy()
    pitch = data["Pitch"].to_numpy()
    heading = data["Heading"].to_numpy()

    # Unclamp heading and calculate sampling frequency.
    heading = utilities.unclamp_signal(heading, 0, 360, 0.9)
    filter_config.sample_frequency = 1 / np.mean(time[1:] - time[0:-1])

    # --------------------------------------------------------------------------
    # ---- Filtering. ----------------------------------------------------------
    # --------------------------------------------------------------------------

    # Add end values.
    signals = np.stack((roll, pitch, heading))
    signals = filters.add_appendage(signals, filter_config)

    # Filter data and adjust for time delay.
    filtered_signals, filter_delay = filters.FIR_filter(signals, \
        filter_config, axis=1)
    filtered_time = time - filter_delay

    print("\nGyroscope:")
    print(" - Sampling time:      {0:.4f}".format( \
        1 / filter_config.sample_frequency))
    print(" - Sampling frequency: {0:.4f}".format( \
        filter_config.sample_frequency))
    print(" - Filter time delay:  {0:.4f}".format(filter_delay))

    # Remove end values.
    filtered_signals = filters.remove_appendage(filtered_signals, \
        filter_config)

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
        time = datetime.datetime.fromtimestamp(epoch).strftime( \
		    "%Y:%m:%d:%H:%M:%S.%f")
        times.append(time)

    filtered_data["Datetime"] = np.array(times, dtype=str)

    # --------------------------------------------------------------------------
    # ---- Plotting. -----------------------------------------------------------
    # --------------------------------------------------------------------------
    
    # Roll plot.
    fig1, ax1 = plt.subplots(figsize=(4, 4))
    ax1.plot(data["Epoch"] - data["Epoch"][0], data["Roll"], \
        linewidth=1.0, label="Unfiltered")
    ax1.plot(filtered_data["Epoch"] - data["Epoch"][0], \
	    filtered_data["Roll"], linewidth=1.0, label="Filtered")
    ax1.set_xlim(time_limits)
    ax1.set_ylim(roll_limits)
    ax1.set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax1.set_ylabel(r"Roll, $\theta$ $[\text{deg}]$")
    ax1.legend()

    # Pitch plot.
    fig2, ax2 = plt.subplots(figsize=(4, 4))
    ax2.plot(data["Epoch"] - data["Epoch"][0], data["Pitch"], \
        linewidth=1.0, label="Unfiltered")
    ax2.plot(filtered_data["Epoch"] - data["Epoch"][0], \
	    filtered_data["Pitch"], linewidth=1.0, label="Filtered")
    ax2.set_xlim(time_limits)
    ax2.set_ylim(pitch_limits)
    ax2.set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax2.set_ylabel(r"Pitch, $\phi$ $[\text{deg}]$")
    ax2.legend()

    # Heading plot.
    fig3, ax3 = plt.subplots(figsize=(4, 4))
    ax3.plot(data["Epoch"] - data["Epoch"][0], data["Heading"], \
        linewidth=1.0, label="Unfiltered")
    ax3.plot(filtered_data["Epoch"] - data["Epoch"][0], \
	    filtered_data["Heading"], linewidth=1.0, label="Filtered")
    ax3.set_xlim(time_limits)
    ax3.set_ylim(heading_limits)
    ax3.set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax3.set_ylabel(r"Heading, $\psi$ $[\text{deg}]$")
    ax3.legend()

    if data_config.show_figures:
        plt.show()

    # --------------------------------------------------------------------------
    # ---- Save data. ----------------------------------------------------------
    # --------------------------------------------------------------------------

    if data_config.save_figures:
        fig1.savefig(data_config.output + "ROV-Gyroscope-Roll.eps", \
            dpi=300)
        fig2.savefig(data_config.output + "ROV-Gyroscope-Pitch.eps", \
            dpi=300)
        fig3.savefig(data_config.output + "ROV-Gyroscope-Heading.eps", \
            dpi=300)

    if data_config.save_output:
        filtered_data = pd.DataFrame(filtered_data)
        filtered_data.to_csv(data_config.output + "ROV-Gyroscope.csv", \
            sep=',')

def main():
    # Plot limits.
    time_limits = [450, 480]
    roll_limits = [0, 5]
    pitch_limits = [0, 8]
    heading_limits = [140, 180]

    # Parse arguments.
    parser = argparse.ArgumentParser( \
        description="Filter gyroscope data with a FIR lowpass filter.")
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
    filter_gyroscope(data_config, filter_config, time_limits, roll_limits, \
        pitch_limits, heading_limits)

if __name__ == '__main__':
    main()
