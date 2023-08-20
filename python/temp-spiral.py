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
    fig = plt.figure(figsize = (7,7))
    
    theta = np.linspace(-np.pi/2, 8/6*np.pi, 12)
    label_x = 3.5 * np.cos(-theta)
    label_y = 3.5 * np.sin(-theta)
    for i in range(12):
        plt.annotate(months[i], 
                     (label_x[i], label_y[i]), 
                     size = 16, ha='center', 
                     va='center',
                     rotation = -i/12*360)
        plt.axis([-4,4,-4,4])
    plt.xticks([])
    plt.yticks([])
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

    return fig

setup()

#%% Visualisation

R = TempR(all_temps)
num_years = 144
theta = np.linspace(-np.pi/2, num_years*8/6*np.pi, num_years*12)

plt.close("all")

setup()

year = plt.annotate(str(600//12 + 1880), (0,0), ha = "center", va = "center",
                 bbox = dict(fc="white", lw = 0), size = 16)
for i in range(600,len(theta)):
    
    R_pair_i = R[i:i+2]
    theta_pair_i = theta[i:i+2]
    
    avgTemp = np.mean(all_temps[i:i+2])
    
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
    plt.plot(x_pair_i, y_pair_i, zorder = 1,
             color = (red, green, blue))
    year.remove()
    year = plt.annotate(str(i//12 + 1880), (0,0), ha = "center", va = "center",
                 bbox = dict(fc="white", lw = 0), size = 16)
    
    plt.pause(0.001)