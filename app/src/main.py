'''
Created on Aug 29, 2017

@author: Hossein
'''
from requests import Session
import json
from email_handler import send_email

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
  with open(file_name) as f: 
    file_text = f.read()
  
  return json.loads(file_text)



if __name__ == "__main__": 
  team_members = get_team_members()
  print(team_members)
  team_data = {'date': team_members}
  # Get the page url for a member 
  page_url = team_members[0]['pageUrl']
  donor_page = get_memeber_page(page_url)
  
  # test if the 'ericssoncommunity' can be found in the page
  assert donor_page[page_url].find('ericssoncommunity') != -1
  
  # Save to file
  save_to_file(data_file_name, team_data)
  
  print("Sending email ... ")
  send_email(data_file_name)

  print("Done!")
  
  
  

