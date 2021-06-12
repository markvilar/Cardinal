import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import numpy as np
import pandas as pd

def rolling_window_filter(data, mode='rolling', window=262, threshold=3):
    """
    Mark as outliers the points that are out of the interval:
    (mean - threshold * std, mean + threshold * std ).
    
    Parameters
    ----------
    data : pandas.Series
        The time series to filter.
    mode : str, optional, default: 'rolling'
        Whether to filter in rolling or expanding basis.
    window : int, optional, default: 262
        The number of periods to compute the mean and standard
        deviation.
    threshold : int, optional, default: 3
        The number of standard deviations above the mean.
        
    Returns
    -------
    series : pandas.DataFrame
        Original series and marked outliers.
    """

    msg = f"Type must be of pandas.Series but {type(data)} was passed."
    assert isinstance(data, pd.Series), msg
    
    series = data.copy()
    
    # rolling/expanding objects
    pd_object = getattr(series, mode)(window=window)
    mean = pd_object.mean()
    std = pd_object.std()
    
    upper_bound = mean + threshold * std
    lower_bound = mean - threshold * std
    
    outliers = ~series.between(lower_bound, upper_bound)
    # fill false positives with 0
    outliers.iloc[:window] = np.zeros(shape=window, dtype=bool)
    
    series = series.to_frame()
    series["Outliers"] = np.array(outliers.values)
    series.columns = ["Values", "Outliers"]
    
    return series

def main():
    path = "/home/martin/dev/Cardinal/Data/Raw/ROV-APS.csv"
    show = False
    save = True

    aps = pd.read_csv(path)
    time = aps["Epoch"]
    northing = aps["UTM Northing"]
    easting = aps["UTM Easting"]
    depth = aps["Depth"]

    planar_window = 10 # 10
    planar_threshold = 2.4 # 2.25
    depth_window = 10
    depth_threshold = 3.0

    northing = rolling_window_filter(northing, window=planar_window, \
        threshold=planar_threshold)
    easting = rolling_window_filter(easting, window=planar_window, \
        threshold=planar_threshold)
    depth = rolling_window_filter(depth, window=depth_window, \
        threshold=depth_threshold)

    mask = np.logical_or(northing["Outliers"], easting["Outliers"])
    mask = np.logical_or(mask, depth["Outliers"])

    fig1, ax1 = plt.subplots(nrows=3, ncols=1, figsize=(7, 4.5))
    fig1.tight_layout(pad=2.0, w_pad=2.0, h_pad=2.0)
    
    ax1[0].plot(time, northing["Values"])
    ax1[0].scatter(time[mask], northing["Values"][mask], color="r")
    ax1[0].set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax1[0].set_ylabel(r"Northing, $N$ $[\text{m}]$")
    ax1[0].set_xlim([ 1611313080, 1611314600 ])
    ax1[0].set_ylim([ 7066350, 7066390 ])

    ax1[1].plot(time, easting["Values"])
    ax1[1].scatter(time[mask], easting["Values"][mask], color="r")
    ax1[1].set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax1[1].set_ylabel(r"Easting, $E$ $[\text{m}]$")
    ax1[1].set_xlim([ 1611313080, 1611314600 ])
    ax1[1].set_ylim([ 597780, 597880 ])

    ax1[2].plot(time, depth["Values"], label="Samples")
    ax1[2].scatter(time[mask], depth["Values"][mask], color="r", \
        label="Outliers")
    ax1[2].set_xlabel(r"Time, $t$ $[\text{s}]$")
    ax1[2].set_ylabel(r"Depth, $D$ $[\text{m}]$")
    ax1[2].set_xlim([ 1611313080, 1611314600 ])
    ax1[2].set_ylim([ -10, 75])

    lg1 = fig1.legend(bbox_to_anchor=(1, 1), loc="upper right", frameon=True, \
        fancybox=False)
    fr1 = lg1.get_frame()
    fr1.set_facecolor("white")
    fr1.set_edgecolor("black")

    if save:
        fig1.savefig("/home/martin/dev/Cardinal/Output/ROV-APS-Outliers.pdf", \
            dpi=300)

    if show:
        plt.show()

if __name__ == "__main__":
    main()
