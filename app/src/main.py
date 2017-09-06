'''
Created on Aug 29, 2017

@author: Hossein
'''
from requests import Session
import argparse
import json
import os 
from email_handler import send_email
from utils import get_raw_data_path
import logging
from tqdm import tqdm

file_name_member_data = 'member_data.txt'
file_name_supporter_data = 'supporter_data.txt'


def get_team_members():
  '''
  Get the data from the web. This tries to imitate the 'function getTeamMembers() {' in the 
  source code of the website here: view-source:https://secure.e2rm.com/registrant/TeamFundraisingPage.aspx?teamID=738302&langPref=en-CA
  return: 
    :list a list containing dictionaries of team members and their raised fund. 
          example: 
          [{'name': 'Johanna Nicoletta', 'isTeamCaptain': 'True', 'amount': '$277.38', 'facebookId': '1633682560', 'pageUrl': 'https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3697209&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA'}, {'name': 'Ericsson Activities', 'isTeamCaptain': 'False', 'amount': '$194.00', 'facebookId': '', 'pageUrl': 'https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3877056&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA'}, {'name': 'Alireza Mirzaee', 'isTeamCaptain': 'False', 'amount': '$25.00', 'facebookId': '', 'pageUrl': 'https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3869108&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA'}, {'name': 'Hossein Seyedmehdi', 'isTeamCaptain': 'False', 'amount': '$0.00', 'facebookId': '', 'pageUrl': 'https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3855399&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA'}]

  '''
  url_ajax_request = "https://secure.e2rm.com/registrant/WebServices/RegistrantWebService.asmx/GetTeamMembers"
  session = Session()
  # to get the payload, use the Chrome Developer Mode (alt+command+I in Mac) >> Network >> XHR >> GetTeamMembers >> Headers >> Request Payload  
  payload = json.dumps({'teamID':738302,
                        'languageCode':'en-CA',
                        'sourceReferrerUrl':'https://secure.e2rm.com/registrant/search.aspx?eventid=210107&langpref=en-CA',
                        'anonymousText':'Anonymous',
                        'isOrderByAmount':'true'})
  response = session.post(url = url_ajax_request, data = payload, headers={'content-type':'application/json'})
  response_dict = response.json()
  team_members = json.loads(response_dict['d'])
  return team_members

def get_member_page(url):
  '''
  Get the page for the list of all_supporters to a team member and returns it as a str blob 
  return: 
    :str : a str representing the page
  '''
  session = Session()
  r = session.get(url)
  return r.text

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
    return 

def update_ledger(ledger, new_data, date = None):
  '''
  A ledger is a dictionary of the history of data. The format of a ledger would be 
  {'a_date': a_data_blob, 'another_date': another_data_blob, ... } 
  If the date exists in the ledger, this function would replace the data for 
  that date with the new_data; otherwise, it will add a new entry with the new data
  and date
  input: 
    :dict : the ledger 
    :any_mutable_object
    :str : in the format of 'YYYYMMDD'. If the date is not given, today's date is used. 
  return: 
    :dict : inplace update of the ledger 
  '''
  #get the date: 
  if not date: 
    from time import gmtime, strftime
    date = strftime("%Y%m%d", gmtime())
  if type(ledger) != type(dict()):
    raise(Exception("ledger should be a dictionary"))
  ledger[date] = new_data
  return 

def parse_member_page(html_page):
  '''
  this function takes the page of a member in raw html format and parses it.
  input
    :str : a raw html 
  return
    :list : a list of dictionaries for supporters in the format of [{'name':'a_name', ...}, {...}, ...] 
  '''
  supporters = []
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(html_page, 'html.parser')
  timeline_items = soup.find_all(class_="timeline-item")
  #print(timeline_items[0])
  for ti in timeline_items:
    # get the content of a supporter. I know! '3' is a magic number, but after some digging the was set.
    supporter_info = list(ti.contents[3].stripped_strings)
    d = {}
    d['supporter_name'] = supporter_info[0]
    d['amount_dollar'] = supporter_info[1][supporter_info[1].find('$') + 1:]
    d['time'] = supporter_info[3]
    d['message'] = ''
    if len(supporter_info) > 4: 
      d['message'] = supporter_info[4]
    supporters.append(d)
  return supporters

if __name__ == "__main__": 
  parser = argparse.ArgumentParser(description='Data analytics and Visualization for LightTheNight (DaViL)')
  parser.add_argument('--no-email', dest='send_email', default=True, action='store_false')

  args = parser.parse_args()

  # get the absolute path to the data files
  team_data_file = os.path.join(get_raw_data_path(), file_name_member_data)
  supporters_data_file = os.path.join(get_raw_data_path(), file_name_supporter_data)

  team_members = get_team_members()

  # update the ledger file with new team member data
  team_ledger = load_from_file(team_data_file)
  update_ledger(team_ledger, team_members)
  save_to_file(team_data_file, team_ledger)

  #
  # get each team member's page showing the supporters and detailed amoutn of donations
  #
  print("Getting all the pages for team members...")
  all_supporters = {}
  for member in tqdm(team_members): 
    p_url = member['pageUrl']
    name = member['name']
    all_supporters[name] = parse_member_page(get_member_page(p_url))
    
  #update the supporter's ledger in the files
  ledger_supporters = load_from_file(supporters_data_file)
  update_ledger(ledger_supporters, all_supporters)
  save_to_file(supporters_data_file, ledger_supporters)

  if args.send_email:
    print("Sending e-mail...")
    #send_email(get_raw_data_path())

  print("Done!")
