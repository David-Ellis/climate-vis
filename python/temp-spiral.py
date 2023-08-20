# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 16:46:51 2023

@author: david
"""

import pandas as pd
import numpy as np

#%% Pre-processing
data = pd.read_csv("../data/GLB.Ts+dSST.csv", skiprows=1)
data = data[['Year', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
       'Oct', 'Nov', 'Dec']]

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
       'Oct', 'Nov', 'Dec']

data[data == "***"] = np.nan
data[months] = data[months].astype(float)

