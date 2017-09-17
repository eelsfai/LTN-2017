'''
Created on Sep 6, 2017

@author: Hossein
'''
import os, json, logging

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

def get_admin_data_path():
  '''
  gets the absolute path to the folder that contains the data for admins
  returns: 
    :str : the absolute path to the admin data folder, e.g., /app/data/admin_data/
  ''' 
  return os.path.join(get_data_path(), 'admin_data')

def get_test_path():
  '''
  gets the absolute path to the folder that contains the data for test
  returns: 
    :str : the absolute path to the test data folder, e.g., /app/data/test/
  ''' 
  return os.path.join(get_data_path(), 'test')


def save_to_file(file_name, arg_dict):
  '''
  Save the dictionary of data into a file
  '''
  with open(file_name, 'w') as f: 
    f.write(json.dumps(arg_dict, sort_keys=True, indent=4))
    
def load_from_file(file_name):
  '''
  load the json from the file
  return: 
    :dict
  '''
  try: 
    with open(file_name) as f: 
      file_text = f.read()
    return json.loads(file_text)
  except Exception as e: 
    # log the error and return None in case there is any problem
    logging.error(e)
