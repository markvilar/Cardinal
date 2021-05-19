import argparse
import datetime
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

from typing import Dict, List

import data
import filters
import utilities
import utm

def filter_dvl(data_config: data.DataConfiguration, \
    filter_config: filters.FilterConfiguration):
    """
    """
    # Read data.
    data = pd.read_csv(data_config.input)

    # Extract relevant data for filtering.
    time = data["Epoch"].to_numpy()
    altitude = data["Altitude"].to_numpy()

    # Calculate sampling frequency.
    filter_config.sample_frequency = 1 / np.mean(time[1:] - time[0:-1])

    # Add end values.
    filtered_altitude = filters.add_appendage(altitude, filter_config)

    # Filter data and account for time delay.
    filtered_altitude, filter_delay = filters.FIR_filter(filtered_altitude, \
        filter_config, axis=1)

    filtered_time = time - filter_delay

    print("\nDVL:")
    print(" - Sampling time:      {0:.4f}".format( \
        1 / filter_config.sample_frequency))
    print(" - Sampling frequency: {0:.4f}".format( \
        filter_config.sample_frequency))
    print(" - Filter time delay:  {0:.4f}".format(filter_delay))

    # Remove end values.
    filtered_altitude = filters.remove_appendage(filtered_altitude, \
        filter_config)

    filtered_data = pd.DataFrame()
    filtered_data["Epoch"] = filtered_time
    filtered_data["Altitude"] = filtered_altitude

    # Datetime calculations.
    times = []
    for epoch in filtered_data["Epoch"]:
        time = datetime.datetime.fromtimestamp(epoch).strftime( \
            data_config.datetime_format)
        times.append(time)

    filtered_data["Datetime"] = np.array(times, dtype=str)

    # Save data.
    if data_config.save_output:
        filtered_data = pd.DataFrame(filtered_data)
        filtered_data.to_csv(data_config.output + "ROV-DVL.csv", sep=',')

def main():
    # Parse arguments.
    parser = argparse.ArgumentParser( \
        description="Filter DVL data with a FIR lowpass filter.")
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
    filter_dvl(data_config, filter_config)
    
if __name__ == '__main__':
    main()
