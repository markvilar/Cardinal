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

def filter_aps(data_config: data.DataConfiguration, \
    filter_config: filters.FilterConfiguration, \
    time_limits: List, northing_limits: List, easting_limits: List, \
    depth_limits: List):
    """
    """
    data = pd.read_csv(data_config.input)

    # Extract relevant data for filtering.
    aps_time = data["Epoch"].to_numpy()
    aps_data = np.stack([ data["UTM Northing"], data["UTM Easting"], \
        data["Depth"] ])
    filter_config.sample_frequency = \
        1 / np.mean(aps_time[1:] - aps_time[0:-1])

    # --------------------------------------------------------------------------
    # ---- Filtering. ----------------------------------------------------------
    # --------------------------------------------------------------------------


    # Add end values.
    filtered_aps_data = filters.add_appendage(aps_data.copy(), \
        filter_config)

    # Filter data and account for time delay.
    filtered_aps_data, filter_delay = filters.FIR_filter( \
        filtered_aps_data, filter_config, axis=1)
    filtered_aps_time = aps_time - filter_delay

    print("\nAPS:")
    print(" - Sampling time:      {0:.4f}".format( \
        1 / filter_config.sample_frequency))
    print(" - Sampling frequency: {0:.4f}".format( \
        filter_config.sample_frequency))
    print(" - Filter time delay:  {0:.4f}".format(filter_delay))

    # Remove end values.
    filtered_aps_data = filters.remove_appendage(filtered_aps_data, \
        filter_config)

    filtered_data = pd.DataFrame()
    filtered_data["Epoch"] = filtered_aps_time
    filtered_data["UTM Northing"] = filtered_aps_data[0]
    filtered_data["UTM Easting"] = filtered_aps_data[1]
    filtered_data["Depth"] = filtered_aps_data[2]
    filtered_data["UTM Zone"] = data["UTM Zone"]
    filtered_data["UTM Hemisphere"] = data["UTM Hemisphere"]

    # --------------------------------------------------------------------------
    # ---- Latitude / longitude calculations -----------------------------------
    # --------------------------------------------------------------------------


    latitudes, longitudes = [], []
    for northing, easting, zone, hemisphere in \
        zip(filtered_data["UTM Northing"], filtered_data["UTM Easting"], \
            filtered_data["UTM Zone"], filtered_data["UTM Hemisphere"]):
        latitude, longitude = utm.UtmToLatLon(easting, northing, zone, \
            hemisphere)

        latitudes.append(latitude)
        longitudes.append(longitude)

    filtered_data["Latitude"] = np.array(latitudes, dtype=float)
    filtered_data["Longitude"] = np.array(longitudes, dtype=float)
    
    # --------------------------------------------------------------------------
    # ---- Datetime calculations. ----------------------------------------------
    # --------------------------------------------------------------------------

    times = []
    for epoch in filtered_data["Epoch"]:
        time = datetime.datetime.fromtimestamp(epoch).strftime(
            data_config.datetime_format)
        times.append(time)

    filtered_data["Datetime"] = np.array(times, dtype=str)

    # --------------------------------------------------------------------------
    # ---- Plotting. -----------------------------------------------------------
    # --------------------------------------------------------------------------
    
    # Northing plot.
    fig1, ax1 = plt.subplots(figsize=(4, 4))
    ax1.plot(data["Epoch"] - data["Epoch"][0], data["UTM Northing"], \
        linewidth=1.0, label="Unfiltered")
    ax1.plot(filtered_data["Epoch"] - data["Epoch"][0], \
        filtered_data["UTM Northing"], linewidth=1.0, label="Filtered")
    ax1.set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax1.set_ylabel(r"UTM Northing, $N$ $[\text{m}]$")
    ax1.set_xlim(time_limits)
    ax1.set_ylim(northing_limits)
    ax1.legend()

    # Easting plot.
    fig2, ax2 = plt.subplots(figsize=(4, 4))
    ax2.plot(data["Epoch"] - data["Epoch"][0], data["UTM Easting"], \
        linewidth=1.0, label="Unfiltered")
    ax2.plot(filtered_data["Epoch"] - data["Epoch"][0], \
        filtered_data["UTM Easting"], linewidth=1.0, label="Filtered")
    ax2.set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax2.set_ylabel(r"UTM Easting, $E$ $[\text{m}]$")
    ax2.set_xlim(time_limits)
    ax2.set_ylim(easting_limits)
    ax2.legend()

    # Depth plot.
    fig3, ax3 = plt.subplots(figsize=(4, 4))
    ax3.plot(data["Epoch"] - data["Epoch"][0], data["Depth"], \
        linewidth=1.0, label="Unfiltered")
    ax3.plot(filtered_data["Epoch"] - data["Epoch"][0], \
        filtered_data["Depth"], linewidth=1.0, label="Filtered")
    ax3.set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax3.set_ylabel(r"Depth, $D$ $[\text{m}]$")
    ax3.set_xlim(time_limits)
    ax3.set_ylim(depth_limits)
    ax3.legend()
    
    # Planar trajectory plot.
    fig4, ax4 = plt.subplots(figsize=(4, 4))
    ax4.plot(data["UTM Easting"], data["UTM Northing"], \
	    linewidth=1.0, label="Unfiltered") 
    ax4.plot(filtered_data["UTM Easting"], filtered_data["UTM Northing"], \
	    linewidth=1.0, label="Filtered") 
    ax4.set_xlabel(r"UTM Easting, $E$ $[\text{m}]$")
    ax4.set_ylabel(r"UTM Northing, $N$ $[\text{m}]$")
    ax4.axis("Equal")
    ax4.legend()

    # 3D trajectory plot.
    fig5 = plt.figure(figsize=(6, 6))
    ax5 = fig5.add_subplot(111, projection='3d')
    ax5.plot(data["UTM Easting"], data["UTM Northing"], data["Depth"], \
        linewidth=1.0, label="Unfiltered")
    ax5.plot(filtered_data["UTM Easting"], filtered_data["UTM Northing"], \
        filtered_data["Depth"], linewidth=1.0, label="Filtered")
    ax5.invert_zaxis()
    ax5.set_xlabel(r"UTM Easting, $E$ $[\text{m}]$")
    ax5.set_ylabel(r"UTM Northing, $N$ $[\text{m}]$")
    ax5.set_zlabel(r"Depth, $D$ $[\text{m}]$")
    ax5.legend()

    if data_config.show_figures:
        plt.show()

    if data_config.save_figures:
        fig1.savefig(data_config.output + "ROV-APS-Northing.png", dpi=300)
        fig2.savefig(data_config.output + "ROV-APS-Easting.png", dpi=300)
        fig3.savefig(data_config.output + "ROV-APS-Depth.png", dpi=300)
        fig4.savefig(data_config.output + "ROV-APS-Planar-Trajectory.png", \
            dpi=300)
        fig5.savefig(data_config.output + "ROV-APS-Trajectory.png", dpi=300)

    if data_config.save_output:
        filtered_data = pd.DataFrame(filtered_data)
        filtered_data.to_csv(data_config.output + "ROV-APS.csv", sep=',')

def main():
    # Plot limits.
    time_limits = [450, 480]
    northing_limits = [7066362, 7066370]
    easting_limits = [597805, 597811]
    depth_limits = [56, 59]

    # Parse arguments.
    parser = argparse.ArgumentParser( \
        description="Filter APS data with a FIR lowpass filter.")
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
    filter_aps(data_config, filter_config, time_limits, northing_limits, \
        easting_limits, depth_limits)

if __name__ == "__main__":
    main()
