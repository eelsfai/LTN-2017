'''
Created on Sep 6, 2017

@author: Hossein

This file handles all the visualizations. It assumes that the status are ready and it 
contains the function to generate the jpg's  
'''
import os 
from utils import get_visual_data_path
import numpy as np
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#plt.switch_backend('agg')
from datetime import datetime as dt 


IMG_QUALITY = 200 # dpi

def generate_bar_chart(label_value_pairs, file_name = None):
  '''
  generates a bar chart based on values, labels the x-axis with labels, 
  and saves it to a file. 
  input
    :list : a list of lables of the chart. These could be the 
            divisions of organization 
    :list : a list of values for each lable 
    :str : a file_name to save the final result in
  '''
  n = len(label_value_pairs)
  x = np.arange(n)
  labels = list(zip(*label_value_pairs))[0]
  vals = list(zip(*label_value_pairs))[1]
  y = np.array(vals)
  # Clear and create the plot
  plt.clf()
  plt.bar(x, y, facecolor='#ff9999', edgecolor='white', ) # 9999ff ff9999
  # Write values 
  for x1,y1 in zip(x, y):
      plt.text(x1, y1, '$%.0f' % y1, ha='center', va= 'bottom', fontsize = 25)
  # Adjust the y size so that there is room for writings
  plt.ylim(0, 1.2 * max(y) ) 
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


def generate_time_series(time_value_pairs, file_name):
  '''
  generates a xtime series chart based on values, labels the x-axis with xtime, 
  and saves it to a file.
  input
    :list : a list of time_value pairs, e.g., [('YYYY-MM-DD', val_float), (...), ...]  
    :str : a file_name to save the final result in
  '''
  times = list(zip(*time_value_pairs))[0]
  vals = list(zip(*time_value_pairs))[1]
  x = np.array([dt.strptime(t, "%Y-%m-%d") for t in times])
  y = np.array(vals)
  dates = matplotlib.dates.date2num(x)
  #print(dates)
  
  plt.clf()
  plt.plot_date(dates, y, fmt="bo-")
  for loc, spine in plt.axes().axes.spines.items(): 
    if loc != 'bottom': 
      # no spine if it is not at the bottom
      spine.set_color('none')
  #remove y ticks
  plt.yticks([])
  # write the data point values on them
  nlabels = 3
  xy_list = list(zip(x, y))
  if len(xy_list) > nlabels:
    index_list = [] 
    for i in range(nlabels): 
      index_list.append(i * (len(xy_list) // nlabels))
    index_list.append(len(xy_list) - 1)
    for i in index_list: 
      x1, y1 = xy_list[i]
      plt.text(x1, y1, '$%.0f' % y1, ha='right', va= 'bottom', fontsize = 15)
  else:
    for x1, y1 in xy_list : 
      plt.text(x1, y1, '$%.0f' % y1, ha='right', va= 'bottom', fontsize = 15)
    
  plt.gcf().autofmt_xdate()
  plt.ylim(0.75 * min(y), 1.1 * max(y) ) 
  plt.title("LTN - Total fund raised", fontsize=20)
  plt.savefig(file_name, dpi=IMG_QUALITY)


def generate_bar_chart_percentage_raised_from_target(label_value_pairs, file_name = None):
  '''
  generates a bar chart based on values, labels the x-axis with labels, 
  and saves it to a file. 
  input
    :list : a list of lables of the chart. These could be the 
            divisions of organization 
    :list : a list of values for each lable 
    :str : a file_name to save the final result in
  '''
  PercentageRaised = (label_value_pairs[0][1])
  N = len(label_value_pairs)
  ind = np.arange(N)  # the x locations for the groups
  width = 0.35       # the width of the bars

  fig, ax = plt.subplots()
  rects1 = ax.bar(ind, PercentageRaised, width, color='r')
  
  # add some text for labels, title and axes ticks
  ax.set_ylabel('%')
  ax.set_title('Percentage raised from target')
  ax.set_xticks(ind + width / 2)
  ax.set_xticklabels((''))
  plt.ylim(0,100)

  # Save the plot
  plt.savefig(file_name, dpi=IMG_QUALITY)
  


if __name__ == "__main__":
  # generate the bar chart for tema competition 
  file_name = os.path.join(get_visual_data_path(), 'divisions.png')
  l = [('Base Band', 326), ('Radio', 1000), ('Indoor', 20)]
  generate_bar_chart(l,  file_name) 
  
  # generate the total fund raised as a function of time
  file_name = os.path.join(get_visual_data_path(), 'time_series.png')
  time_vals = [('2017-09-01', 100), ('2017-09-02', 200), ('2017-09-04', 310), ('2017-09-05', 400),
        ('2017-09-06', 450), ('2017-09-07', 600), ('2017-09-08', 600), ('2017-09-09', 600),
        ('2017-09-10', 600), ('2017-09-12', 600)]
  generate_time_series(time_vals, file_name)
  
  print('Done!')
  

  
