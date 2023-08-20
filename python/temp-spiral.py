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
                     va='center')
        plt.axis([-4,4,-4,4])
        
    # plot 0, 1, 2 degree circles
    for temp in [0, 1, 2]:
        theta = np.linspace(0, 2*np.pi, 100)
        plt.plot(
            TempR(temp)*np.cos(theta),
            TempR(temp)*np.sin(theta),
            "-", lw = 2, color = "lightgray")
        label = "{}$^oC$".format(temp)
        bbox = dict(fc="white", lw = 0)
        plt.annotate(label, (0,TempR(temp)),
                     ha = "center", va = "center",
                     bbox = bbox)
    plt.xticks([])
    plt.yticks([])
    return fig

#%% Visualisation

setup()