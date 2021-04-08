python Python/filter_aps.py                                   \
    "./Data/Outlier-Filtered/Dive-1/ROV-APS.csv"              \
    "./Output/Filtered/Dive-1/"                               \
    8 0.100 10 --save_figures --save_output                   \

python Python/filter_gyroscope.py                             \
    "./Data/Outlier-Filtered/Dive-1/ROV-Gyroscope.csv"        \
    "./Output/Filtered/Dive-1/"                               \
    6 0.600 10 --save_figures --save_output                   \

python Python/filter_pressure_sensor.py                       \
    "./Data/Outlier-Filtered/Dive-1/ROV-Pressure-Sensor.csv"  \
    "./Output/Filtered/Dive-1/"                               \
    4 0.450 10 --save_figures --save_output                   \

python Python/filter_dvl.py                                   \
    "./Data/Outlier-Filtered/Dive-1/ROV-DVL.csv"              \
    "./Output/Filtered/Dive-1/"                               \
    4 2.000 10 --save_figures --save_output                   \

python Python/filter_aps.py                                   \
    "./Data/Outlier-Filtered/Dive-2/ROV-APS.csv"              \
    "./Output/Filtered/Dive-2/"                               \
    8 0.100 10 --save_figures --save_output                   \

python Python/filter_gyroscope.py                             \
    "./Data/Outlier-Filtered/Dive-2/ROV-Gyroscope.csv"        \
    "./Output/Filtered/Dive-2/"                               \
    6 0.600 10 --save_figures --save_output                   \

python Python/filter_pressure_sensor.py                       \
    "./Data/Outlier-Filtered/Dive-2/ROV-Pressure-Sensor.csv"  \
    "./Output/Filtered/Dive-2/"                               \
    4 0.450 10 --save_figures --save_output                   \

python Python/filter_dvl.py                                   \
    "./Data/Outlier-Filtered/Dive-2/ROV-DVL.csv"              \
    "./Output/Filtered/Dive-2/"                               \
    4 2.000 10 --save_figures --save_output                   \
