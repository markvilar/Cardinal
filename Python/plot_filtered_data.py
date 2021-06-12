import argparse
import datetime

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import numpy as np
import pandas as pd

from typing import Dict, List

def plot_navigation_data(unfiltered: Dict, filtered: Dict, output: str, \
    save: bool, show: bool):
    """
    """
    # ---- APS ----------------------------------------------------------------

    # Northing plot.
    fig1, ax1 = plt.subplots(nrows=3, ncols=1, figsize=(7, 4.5))
    fig1.tight_layout(pad=2.0, w_pad=2.0, h_pad=2.0)

    ax1[0].plot(unfiltered["APS"]["Epoch"], unfiltered["APS"]["UTM Northing"], \
        linewidth=1.0)
    ax1[0].plot(filtered["APS"]["Epoch"], filtered["APS"]["UTM Northing"], \
        linewidth=1.0)
    ax1[0].set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax1[0].set_ylabel(r"Northing, $N$ $[\text{m}]$")
    ax1[0].set_xlim([ 1611313600, 1611313640 ])
    ax1[0].set_ylim([ 7066365, 7066371 ])

    # Easting plot.
    ax1[1].plot(unfiltered["APS"]["Epoch"], unfiltered["APS"]["UTM Easting"], \
        linewidth=1.0)
    ax1[1].plot(filtered["APS"]["Epoch"], filtered["APS"]["UTM Easting"], \
        linewidth=1.0)
    ax1[1].set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax1[1].set_ylabel(r"Easting, $E$ $[\text{m}]$")
    ax1[1].set_xlim([ 1611313600, 1611313640 ])
    ax1[1].set_ylim([ 597806, 597810 ])

    # Depth plot.
    ax1[2].plot(unfiltered["APS"]["Epoch"], unfiltered["APS"]["Depth"], \
        linewidth=1.0, label="Unfiltered")
    ax1[2].plot(filtered["APS"]["Epoch"], filtered["APS"]["Depth"], \
        linewidth=1.0, label="Filtered")
    ax1[2].set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax1[2].set_ylabel(r"Depth, $D$ $[\text{m}]$")
    ax1[2].set_xlim([ 1611313600, 1611313640 ])
    ax1[2].set_ylim([ 57, 58 ])

    lg1 = fig1.legend(bbox_to_anchor=(1, 1), loc="upper right", frameon=True, \
        fancybox=False)
    fr1 = lg1.get_frame()
    fr1.set_facecolor("white")
    fr1.set_edgecolor("black")

    # ---- Gyro ---------------------------------------------------------------

    # Series plot.
    fig2, ax2 = plt.subplots(nrows=3, ncols=1, figsize=(7, 4.5))
    fig2.tight_layout(pad=2.0, w_pad=2.0, h_pad=2.0)

    ax2[0].plot(unfiltered["Gyroscope"]["Epoch"], unfiltered["Gyroscope"]["Roll"], linewidth=1.0)
    ax2[0].plot(filtered["Gyroscope"]["Epoch"], filtered["Gyroscope"]["Roll"], linewidth=1.0)
    ax2[0].set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax2[0].set_ylabel(r"Roll, $\theta$ $[\text{deg}]$")
    ax2[0].set_xlim([ 1611313600, 1611313620 ])
    ax2[0].set_ylim([ 0, 6 ])

    # Pitch plot.
    ax2[1].plot(unfiltered["Gyroscope"]["Epoch"], unfiltered["Gyroscope"]["Pitch"], linewidth=1.0)
    ax2[1].plot(filtered["Gyroscope"]["Epoch"], filtered["Gyroscope"]["Pitch"], linewidth=1.0)
    ax2[1].set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax2[1].set_ylabel(r"Pitch, $\phi$ $[\text{deg}]$")
    ax2[1].set_xlim([ 1611313600, 1611313620 ])
    ax2[1].set_ylim([ -1, 8 ])

    # Heading plot.
    ax2[2].plot(unfiltered["Gyroscope"]["Epoch"], unfiltered["Gyroscope"]["Heading"], linewidth=1.0, \
        label="Unfiltered")
    ax2[2].plot(filtered["Gyroscope"]["Epoch"], filtered["Gyroscope"]["Heading"], \
        linewidth=1.0, label="Filtered")
    ax2[2].set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax2[2].set_ylabel(r"Heading, $\psi$ $[\text{deg}]$")
    ax2[2].set_xlim([ 1611313600, 1611313620 ])
    ax2[2].set_ylim([ 145, 175 ])

    lg2 = fig2.legend(bbox_to_anchor=(1, 1), loc="upper right", frameon=True, \
        fancybox=False)
    fr2 = lg2.get_frame()
    fr2.set_facecolor("white")
    fr2.set_edgecolor("black")

    # ---- DVL ----------------------------------------------------------------

    fig3, ax3 = plt.subplots(figsize=(7, 1.95))

    ax3.plot(unfiltered["DVL"]["Epoch"], unfiltered["DVL"]["Altitude"], \
        linewidth=1.0, label="Unfiltered")
    ax3.plot(filtered["DVL"]["Epoch"], filtered["DVL"]["Altitude"], \
        linewidth=1.0, label="Filtered")
    ax3.set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax3.set_ylabel(r"Altitude, $h$ $[\text{m}]$")
    ax3.set_xlim([ 1611313600, 1611313620 ])
    ax3.set_ylim([ 1.1, 1.9 ])

    lg3 = fig3.legend(bbox_to_anchor=(1, 1), loc="upper right", frameon=True, \
        fancybox=False)
    fr3 = lg3.get_frame()
    fr3.set_facecolor("white")
    fr3.set_edgecolor("black")
    fig3.tight_layout(pad=2.0)

    # ---- PG -----------------------------------------------------------------

    fig4, ax4 = plt.subplots(figsize=(7, 1.95))

    ax4.plot(unfiltered["Pressure"]["Epoch"], unfiltered["Pressure"]["Depth"], \
        linewidth=1.0, label="Unfiltered")
    ax4.plot(filtered["Pressure"]["Epoch"], filtered["Pressure"]["Depth"], \
        linewidth=1.0, label="Filtered")
    ax4.set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax4.set_ylabel(r"Depth, $D$ $[\text{m}]$")
    ax4.set_xlim([ 1611313600, 1611313620 ])
    ax4.set_ylim([ 56.5, 57.7 ])

    lg4 = fig4.legend(bbox_to_anchor=(1, 1), loc="upper right", frameon=True, \
        fancybox=False)
    fr4 = lg4.get_frame()
    fr4.set_facecolor("white")
    fr4.set_edgecolor("black")

    fig4.tight_layout(pad=2.0)

    if show:
        plt.show()

    if save:
        fig1.savefig(output + "ROV-APS-Filtered.pdf", dpi=300)
        fig2.savefig(output + "ROV-Gyroscope-Filtered.pdf", dpi=300)
        fig3.savefig(output + "ROV-DVL-Filtered.pdf", dpi=300)
        fig4.savefig(output + "ROV-PS-Filtered.pdf", dpi=300)

def main():
    output = "/home/martin/dev/Cardinal/Output/"
    save = True
    show = False

    unfiltered_dir = "/home/martin/dev/Cardinal/Data/Outlier-Filtered/Dive-1/"
    unfiltered = {}
    unfiltered["APS"] = pd.read_csv(unfiltered_dir + "ROV-APS.csv")
    unfiltered["Gyroscope"] = pd.read_csv(unfiltered_dir + "ROV-Gyroscope.csv")
    unfiltered["DVL"] = pd.read_csv(unfiltered_dir + "ROV-DVL.csv")
    unfiltered["Pressure"] = pd.read_csv(unfiltered_dir \
        + "ROV-Pressure-Sensor.csv")

    filtered_dir = "/home/martin/dev/Cardinal/Output/Filtered/Dive-1/"
    filtered = {}
    filtered["APS"] = pd.read_csv(filtered_dir + "ROV-APS.csv")
    filtered["Gyroscope"] = pd.read_csv(filtered_dir + "ROV-Gyroscope.csv")
    filtered["DVL"] = pd.read_csv(filtered_dir + "ROV-DVL.csv")
    filtered["Pressure"] = pd.read_csv(filtered_dir + "ROV-Pressure-Sensor.csv")

    # Filter unfiltered.
    plot_navigation_data(unfiltered, filtered, output, save, show)
    
if __name__ == '__main__':
    main()
