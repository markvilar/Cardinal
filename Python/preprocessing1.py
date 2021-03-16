import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib
import datetime


# File for reading from GND format 
initial_time = '12:14:43.200'
time_i = initial_time.split(':')
h = int(time_i[0])
m = int(time_i[1])
s = int(np.floor(float(time_i[2])))
ms = int((float(time_i[2])-s)*1000000)

initial_time_dt = datetime.datetime(2017,3, 7,
                                        h, m, s,ms)
initial_time_epoch = datetime.datetime.timestamp(initial_time_dt)

# Add file to compensate for tide

# Extract the pose measurements
time_pos = []
time_depth = []
time_IMU =[]

x = []
y = []
z = []
z_press = []
yaw =[]
roll =[]
pitch = []
with open('D:/Skogn/Skogn_nav/20210122_100221_G.NPD', 'r') as fp:
    line = fp.readline()
    cnt = 1
    while line:
        line = fp.readline()
        if line[0:4] == 'P  D': # For reading the position data from the transponder on the vehicle
            time_str = line[10:34]
            # Convert to a date time
            time_splitted = time_str.split(':')
            time_dt = datetime.datetime(int(time_splitted[0]),int(time_splitted[1]), int(time_splitted[2]),
                                        int(time_splitted[3]), int(time_splitted[4]), int(np.floor(float(time_splitted[5]))),
                                        int((float(time_splitted[5])-np.floor(float(time_splitted[5])))*1000000))

            # Convert to epoch time
            time_epoch = datetime.datetime.timestamp(time_dt)
            time_pos.insert(len(time_pos), time_epoch)
            #Extract position
            pos_x = float(line[36:47])
            x.insert(len(x),  pos_x)

            pos_y = float(line[49:61])
            y.insert(len(y), pos_y)

            pos_z = float(line[63:71])
            z.insert(len(z), pos_z)

        elif line[0:7] == 'R132  4': # For reading the orientation data from the gyro on the vehicle
            time_str = line[9:32]
            # Convert to a date time
            time_splitted = time_str.split(':')
            time_dt = datetime.datetime(int(time_splitted[0]), int(time_splitted[1]), int(time_splitted[2]),
                                        int(time_splitted[3]), int(time_splitted[4]),
                                        int(np.floor(float(time_splitted[5]))),
                                        int((float(time_splitted[5]) - np.floor(float(time_splitted[5]))) * 1000000))
            # Convert datetime to epoch time
            time_epoch = datetime.datetime.timestamp(time_dt)
            time_IMU.insert(len(time_IMU), time_epoch)
            imu = line.split(',')

            heading = float(imu[3])

            yaw.insert(len(yaw), heading)
            roll.insert(len(roll),float(imu[1]))
            pitch.insert(len(pitch), float(imu[2]))
        elif line[0:14] == 'D     3  19  1':# Reading the depth data
            time_str = line[16:39]
            # Convert to a date time
            time_splitted = time_str.split(':')
            pos_z = float(line[41:48])
            z_press.insert(len(z_press), pos_z)
            time_dt = datetime.datetime(int(time_splitted[0]), int(time_splitted[1]), int(time_splitted[2]),
                                        int(time_splitted[3]), int(time_splitted[4]),
                                        int(np.floor(float(time_splitted[5]))),
                                        int((float(time_splitted[5]) - np.floor(float(time_splitted[5]))) * 1000000))
            # Convert datetime to epoch time
            time_epoch = datetime.datetime.timestamp(time_dt)
            time_depth.insert(len(time_depth), time_epoch)





#filename = 'D:/GIS/nav.txt'

#df_navigation = pd.read_csv(filename, sep=',', header=1)
#
#np.save('z_tide', tide_z)
#np.save('z_tide_time', tide_time)
#
#plt.show()

# Save x_position and position time
np.save('x_tp', x)
np.save('time_usbl', np.array(time_pos))
# Save y position
np.save('y_tp', y)
# Save z-position and time
np.save('z_digiquartz', z_press)
np.save('depth_time', np.array(time_depth))
# Save IMU data and
np.save('yaw', yaw)
np.save('pitch',pitch)
np.save('roll', roll)
np.save('time_IMU', np.array(time_IMU))

