# -*- coding: utf-8 -*-
"""
Created on Sat May 28 15:45:40 2022

@author: Audrey
"""

import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('Data_by_Adj_2.csv')
bare_data = [dat[a_1], data_2, data_3, data_4]
 
fig = plt.figure(figsize =(10, 7))
 
# Creating axes instance
ax = fig.add_axes([0, 0, 1, 1])
 
# Creating plot
bp = ax.boxplot(data)