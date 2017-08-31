'''
Created on Aug 30, 2017

@author: Hossein
'''
import unittest
from . import main

class TestScrapingMethods(unittest.TestCase):
  '''
  Test the methods used to collect data from the web, save into and load from files. 
  '''
  def test_make_ajax_request(self):
    team_members = main.make_ajax_request()
    found_Johanna = False
    for d in team_members: 
      if d['name'] == 'Johanna Nicoletta': 
        found_Johanna = True
    self.assertEqual(found_Johanna, True, "The AJAX call was not successful!")
    
  def test_save_and_load(self):
    team_members = main.make_ajax_request()
    team_data = {'date': team_members}
    # save data to file 
    data_file_name = 'web_data_json_test.data'

    main.save_to_file(data_file_name, team_data)    
    #
    # test loading from the file and if the name of Johanna can be found
    #
    print('loading from the file...')
    member_data = main.load_from_file(data_file_name)
    a_day_data = {}
    # take the first item in the dictionary; doesn'e matter which one it is
    for key in member_data: 
      a_day_data = member_data[key]
      break
    found_Johanna = False
    for d in a_day_data: 
      if d['name'] == 'Johanna Nicoletta': 
        found_Johanna = True
    self.assertEqual(found_Johanna, True, "Can not save or load from file")

    