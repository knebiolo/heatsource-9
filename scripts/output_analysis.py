# -*- coding: utf-8 -*-
"""
Created on Thu May  9 09:52:46 2024

@author: Kevin.Nebiolo

Script Intent: 
    Refactor R code written by L. Gardner into Python to analyze heatsource output.
"""

# import modules
import pandas as pd
import os

# identify workspace
inputWS = r"C:\Users\knebiolo\Desktop\heatsource\output\Scenario_1a_ExistingCondition_2018Lidar_TFT_Channel"

# get data
data = pd.read_csv(os.path.join(inputWS,'Temp_H2O.csv'),skiprows = 6)
data_long = data.melt(id_vars=['Datetime'], var_name='RKM', value_name='Temp')
data_long['Datetime'] = pd.to_timedelta(data_long.Datetime, unit = 'D') + pd.Timestamp('1899-12-31')
data_long['Day'] =  data_long.Datetime.dt.day

# quantify daily change
daily_min = data_long.groupby(['RKM','Day'])['Temp'].min()
daily_max = data_long.groupby(['RKM','Day'])['Temp'].max()
daily_avg = data_long.groupby(['RKM','Day'])['Temp'].mean()

# Concatenate into a DataFrame
daily_stats = pd.concat([daily_min, daily_max, daily_avg], axis=1)
daily_stats.columns = ['MinTemp', 'MaxTemp', 'AvgTemp']

# calculate 7 day moving average of daily maximum
daily_stats['SevenDay'] = daily_stats.groupby('RKM')['MaxTemp'].rolling(window=7).mean().reset_index(level=0, drop=True)

# get Max Seven Day per RKM
max_7_day = daily_stats.groupby('RKM')['SevenDay'].max()

