# -----------------------------------------------------------------------------
# ---- Dive 1 -----------------------------------------------------------------
# -----------------------------------------------------------------------------

python Python/filter_hipap.py                            \
    "./Data/Outlier-Filtered/Dive-1/ROV-HiPAP.csv"       \
    "./Output/Filtered/Dive-1/"                          \
    8 0.2 10 --save_figures --save_output                \

python Python/filter_gyrocompass.py                      \
    "./Data/Outlier-Filtered/Dive-1/ROV-Gyrocompass.csv" \
    "./Output/Filtered/Dive-1/"                          \
    6 0.1 10 --save_figures --save_output                \

python Python/filter_dvl.py                              \
    "./Data/Outlier-Filtered/Dive-1/ROV-DVL.csv"         \
    "./Output/Filtered/Dive-1/"                          \
    6 0.2 10 --save_figures --save_output                \

python Python/filter_digiquartz.py                       \
    "./Data/Outlier-Filtered/Dive-1/ROV-Digiquartz.csv"  \
    "./Output/Filtered/Dive-1/"                          \
    4 0.3 10 --save_figures --save_output                \

# -----------------------------------------------------------------------------
# ---- Dive 2 -----------------------------------------------------------------
# -----------------------------------------------------------------------------

python Python/filter_hipap.py                            \
    "./Data/Outlier-Filtered/Dive-2/ROV-HiPAP.csv"       \
    "./Output/Filtered/Dive-2/"                          \
    8 0.2 10 --save_figures --save_output                \

python Python/filter_gyrocompass.py                      \
    "./Data/Outlier-Filtered/Dive-2/ROV-Gyrocompass.csv" \
    "./Output/Filtered/Dive-2/"                          \
    6 0.1 10 --save_figures --save_output                \

python Python/filter_dvl.py                              \
    "./Data/Outlier-Filtered/Dive-2/ROV-DVL.csv"         \
    "./Output/Filtered/Dive-2/"                          \
    6 0.2 10 --save_figures --save_output                \

python Python/filter_digiquartz.py                       \
    "./Data/Outlier-Filtered/Dive-2/ROV-Digiquartz.csv"  \
    "./Output/Filtered/Dive-2/"                          \
    4 0.3 10 --save_figures --save_output                \
