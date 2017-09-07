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


def generate_bar_chart(labels= [], values = [], file_name = None):
  '''
  generates a bar chart and saves it to a file. 
  input
    :list : a list of lables of the chart. These could be the divisions of organization 
    :list : a list of values for each lable 
    :str : a file_name to save the final result in
  '''
    
  if len(labels) != len(values):
    raise ValueError("The size of lables and values must be equal.")
  n = len(labels)
  x = np.arange(n)
  y = np.array(values)
  
  plt.bar(x, y, facecolor='#ff9999', edgecolor='white', )
  #plt.bar(x, y, facecolor='#9999ff', edgecolor='white', )
  #plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')
  
  for x1,y1 in zip(x, y):
      plt.text(x1, y1, '$%.0f' % y1, ha='center', va= 'bottom', fontsize = 25)
  
  #plt.xlim(-.5, n ) 
  plt.ylim(0, 1.2 * max(values) ) 
  plt.xticks(x, labels, fontsize = 15)
  # no y axis ticks
  plt.yticks([])
  plt.title("Light The Night fundraising results", fontsize = 20)
  # remove all the spines except the bottom one [trick here](https://stackoverflow.com/questions/18968024/how-to-remove-axis-in-pyplot-bar)
  for loc, spine in plt.axes().axes.spines.items(): 
    if loc != 'bottom': 
      spine.set_color('none')
  
  plt.savefig(file_name, dpi=200)

if __name__ == "__main__":
  file_name = os.path.join(get_visual_data_path(), 'divisions.jpg')
  v = [326, 5000, 20]
  l = ['Base Band', 'Radio', 'Indoor']
  generate_bar_chart(labels= l, values= v, file_name= file_name) 
  print('Done!')
  
  
