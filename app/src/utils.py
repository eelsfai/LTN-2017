'''
Created on Sep 6, 2017

@author: Hossein
'''
import os 

def get_data_path():
  '''
  Gets the path of the "data" directory, which will have subdirectories
  for different data files.

  returns:
    :str : Absolute path to the "data" directory.
  '''
  script_dirname = os.path.dirname(os.path.abspath(__file__))
  return os.path.join(script_dirname, '..', 'data')

def get_raw_data_path():
  '''
  gets the absolute path to the folder for the raw data
  returns: 
    :str : the absolute path to the data folder, e.g., /app/data/raw_data/
  ''' 
  return os.path.join(get_data_path(), 'raw_data')

def get_visual_data_path():
  '''
  gets the absolute path to the folder that contains the visualization data
  returns: 
    :str : the absolute path to the visualized data folder, e.g., /app/data/visual_data/
  ''' 
  return os.path.join(get_data_path(), 'visual_data')
