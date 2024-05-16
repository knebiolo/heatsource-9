# -*- coding: utf-8 -*-
"""
Created on Sat May  4 10:10:09 2024

@author: Kevin.Nebiolo
"""

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Load your data
data = pd.read_csv(r'C:\Users\knebiolo\Desktop\temperature.csv')
data['Datetime'] = pd.to_datetime(data['Datetime'])  # Convert to datetime if necessary

joydata = data.iloc[:, :100]
plotlydata = data

#%% Joy Division Style Plot
# Convert 'Datetime' to days since the start for plotting
joydata['Days'] = (joydata['Datetime'] - joydata['Datetime'].min()).dt.total_seconds() / (24 * 3600)

# Set up the figure and axis for 3D plotting
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Get x, y, z values for plotting
x = joydata['Days']
y_labels = joydata.columns[1:-1]  # Adjust this if your dataframe structure is different
Y, X = np.meshgrid(y_labels, x)

# Normalize Z values for visual effect in a Joy Division style
Z = joydata.drop(['Datetime', 'Days'], axis=1).values
Z_normalized = (Z - Z.mean(axis=0)) / Z.std(axis=0)

# Plot each column as a separate line
for i, y in enumerate(y_labels):
    ax.plot(X[:, i], np.full(X[:, i].shape, y), Z_normalized[:, i], color='k', linewidth=0.5)

# Setting labels and title
ax.set_xlabel('Days since start')
ax.set_ylabel('River Kilometer')
ax.set_zlabel('Normalized Temperature')
ax.set_title('Joy Division Style Temperature Plot Along River')

# Hide grid lines and ticks for aesthetics
ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

plt.show()

#%% Plotly Intereactive Plot

# Example column name for plotting, replace '11.15' with the actual column name you want to start with
initial_km = '11.15'

# Create the initial time series plot
fig = px.line(plotlydata, x='Datetime', y=initial_km, title='Temperature Time Series',
              labels={'Datetime': 'Date Time', initial_km: 'Temperature (°C)'})

# Create dropdown options for all kilometer columns
km_options = [{'label': km, 'method': 'update', 'args': [{'y': [plotlydata[km].values]}, {'yaxis': {'title': 'Temperature (°C)'}}]}
               for km in plotlydata.columns[1:] if km != 'Datetime']  # Adjust based on your dataframe structure

# Add dropdown menu to the figure
fig.update_layout(
    updatemenus=[{
        'buttons': km_options,
        'direction': 'down',
        'showactive': True,
        'x': 0.1,
        'xanchor': 'left',
        'y': 1.1,
        'yanchor': 'top'
    }]
)

fig.show()
