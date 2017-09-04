'''
Created on Aug 29, 2017

@author: Hossein
'''
from requests import Session
import json
import os 
from email_handler import send_email, get_raw_data_path
from app.src.email_handler import get_raw_data_path

data_file_name = 'web_data_json.txt'


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

def get_memeber_page(url):
  '''
  Get the page for the list of donors to a team member and returns it as a str blob 
  return: 
    : {'url' : 'a_str_representing_the_page'}
  '''
  session = Session()
  r = session.get(url)
  result = {url : r.text} 
  return result

def save_to_file(file_name, arg_dict):
  '''
  Save the dictionary of data into a file
  '''
  with open(file_name, 'w') as f: 
    f.write(json.dumps(arg_dict))
    
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
  except: 
    return 

def update_ledger(ledger, new_data, date = None):
  '''
  A ledger is a dictionary of the history of data. The format of a ledger would be 
  {'a_date': a_data_blob, 'nother_date': another_data_blob, ... } 
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

if __name__ == "__main__": 
  # get the absolute path to the data file
  team_data_file = os.path.join(get_raw_data_path(), data_file_name)

  team_members = get_team_members()
  
  # Get the page url for a member 
  #page_url = team_members[0]['pageUrl']
  #donor_page = get_memeber_page(page_url)
  
  # test if the 'ericssoncommunity' can be found in the page
  #assert donor_page[page_url].find('ericssoncommunity') != -1
  
  # update the ledger file with new team member data
  team_ledger = load_from_file(team_data_file)
  update_ledger(team_ledger, team_members)
  save_to_file(team_data_file, team_ledger)
  print(json.dumps(team_ledger, indent=4))
    
  
  #print("Sending email ... ")
  #send_email(data_file_name)

  print("Done!")
  
  
  

