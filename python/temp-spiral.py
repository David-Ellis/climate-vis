# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 16:46:51 2023

@author: david
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% Pre-processing
data = pd.read_csv("../data/GLB.Ts+dSST.csv", skiprows=1)
data = data[['Year', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
       'Oct', 'Nov', 'Dec']]

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
       'Oct', 'Nov', 'Dec']

data[data == "***"] = np.nan
data[months] = data[months].astype(float)

all_temps = np.concatenate(data[months].values)


#%% Setup

def TempR(temp):
    # convert temperature into radius
    return temp + 1

def setup():
    theta = np.linspace(-np.pi/2, 8/6*np.pi, 12)
    label_x = 3.3 * np.cos(-theta)
    label_y = 3.3 * np.sin(-theta)
    
    
    plt.axis([-4,4,-4,4])
    plt.xticks([])
    plt.yticks([])
    
    for i in range(12):
        plt.annotate(months[i], 
                     (label_x[i], label_y[i]), 
                     size = 16, ha='center', 
                     va='center',
                     rotation = -i/12*360)

    # plot 0, 1, 2 degree circles
    for temp in [0, 1, 2]:
        theta = np.linspace(0, 2*np.pi, 100)
        plt.plot(
            TempR(temp)*np.cos(theta),
            TempR(temp)*np.sin(theta),
            "-", lw = 2, color = "lightgray",
            zorder = 0)
        label = "{}$^oC$".format(temp)
        bbox = dict(fc="white", lw = 0)
        plt.annotate(label, (0,TempR(temp)),
                     ha = "center", va = "center",
                     bbox = bbox, zorder = 0)
        
#%% Visualisation 

def frame(frame_num, year):        
    index = frame_num
    R_pair_i = R[index:index+2]
    theta_pair_i = np.array([-np.pi/2 + frame_num * np.pi/6,
                    -np.pi/2 + (frame_num + 1) * np.pi/6])
    
    avgTemp = np.mean(all_temps[index:index+2])
    
    if avgTemp >= 0:
        red = 0.8
        green = max(0, 0.8 - avgTemp)
        blue = max(0, 0.8 - avgTemp)
    else:
        red = max(0, 0.8 + avgTemp)
        green = max(0, 0.8 + avgTemp)
        blue = 0.8
    
    x_pair_i = R_pair_i*np.cos(-theta_pair_i)
    y_pair_i = R_pair_i*np.sin(-theta_pair_i)
    
    ax.plot(x_pair_i, y_pair_i, zorder = 1,
          color = (red, green, blue))
    year.remove()
    year = ax.annotate(str(index//12 + 1880), (0,0), 
                  ha = "center", va = "center",
                  bbox = dict(fc="white", lw = 0), size = 16)

    return(year)
    
fig = plt.figure(figsize = (7,7))
ax = fig.add_subplot(111)

setup()

R = TempR(all_temps)
num_frames = 1000
num_years = 144
skip = 144*4

year = ax.annotate(str(0) , (0,0), 
                  ha = "center", va = "center",
                  bbox = dict(fc="white", lw = 0), size = 16)
ax.set_title("Global-mean monthly temperature (L-OTI)", size = 16)

for i in range(skip, 1726):
    year = frame(i, year)
    plt.savefig("../figures/spiral/{}.png".format(i), 
                bbox_inches = "tight")


#%% Convert to gif

from PIL import Image

images = []

for i in range(skip, 1726):
    im = Image.open("../figures/spiral/{}.png".format(i))
    images.append(im)

#%%
images[0].save('../figures/spiral.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)
