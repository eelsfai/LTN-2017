'''
Created on Sep 6, 2017

@author: Hossein

This file handles all the visualizations. It assumes that the status are ready and it 
contains the function to generate the jpg's  
'''
import os 
from utils import get_visual_data_path
import numpy as np
import matplotlib.pyplot as plt
from turtledemo.__main__ import font_sizes

IMG_QUALITY = 200 # dpi

def generate_bar_chart(labels, values, file_name = None):
  '''
  generates a bar chart based on values, labels the x-axis with labels, 
  and saves it to a file. 
  input
    :list : a list of lables of the chart. These could be the 
            divisions of organization 
    :list : a list of values for each lable 
    :str : a file_name to save the final result in
  '''
  if len(labels) != len(values):
    raise ValueError("The size of lables and values must be equal.")
  n = len(labels)
  x = np.arange(n)
  y = np.array(values)
  # Clear and create the plot
  plt.clf()
  plt.bar(x, y, facecolor='#ff9999', edgecolor='white', ) # 9999ff ff9999
  # Write values 
  for x1,y1 in zip(x, y):
      plt.text(x1, y1, '$%.0f' % y1, ha='center', va= 'bottom', fontsize = 25)
  # Adjust the y size so that there is room for writings
  plt.ylim(0, 1.2 * max(values) ) 
  plt.xticks(x, labels, fontsize = 15)
  # no y axis ticks
  plt.yticks([])
  plt.title("Light The Night fundraising results", fontsize = 20)
  # Remove all the spines except the bottom one 
  # [trick here](https://stackoverflow.com/questions/18968024/how-to-remove-axis-in-pyplot-bar)
  for loc, spine in plt.axes().axes.spines.items(): 
    if loc != 'bottom': 
      # no spine if it is not at the bottom
      spine.set_color('none')
  # Save the plot
  plt.savefig(file_name, dpi=IMG_QUALITY)


def generate_time_series(xtime, values, file_name):
  '''
  generates a xtime series chart based on values, labels the x-axis with xtime, 
  and saves it to a file.
  input
    :list : a list of times  
    :list : a list of values for each xtime 
    :str : a file_name to save the final result in
  '''
  if len(xtime) != len(values):
    raise ValueError("The size of lables and values must be equal.")

  from datetime import datetime as dt 
  print(dt.strptime(xtime[0], "%Y-%m-%d"))
  x = np.array([dt.strptime(t, "%Y-%m-%d") for t in xtime])
  print(x)
  y = np.array(values)
  plt.clf()
  plt.plot(x, values)
  plt.savefig(file_name, dpi=IMG_QUALITY)

if __name__ == "__main__":
  file_name = os.path.join(get_visual_data_path(), 'divisions.jpg')
  v = [326, 5000, 20]
  l = ['Base Band', 'Radio', 'Indoor']
  generate_bar_chart(l, v,  file_name) 
  
  file_name = os.path.join(get_visual_data_path(), 'time_series.jpg')
  t = ['2017-09-01', '2017-09-02', '2017-09-04']
  v_ = [10, 20, 30]
  generate_time_series(t, v_, file_name)
  print('Done!')
  
  
