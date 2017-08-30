'''
Created on Aug 29, 2017

@author: Hossein
'''
from requests import Session
import json

url_main_team_page = "https://secure.e2rm.com/registrant/TeamFundraisingPage.aspx?teamID=738302&langPref=en-CA"
url_ajax_request = "https://secure.e2rm.com/registrant/WebServices/RegistrantWebService.asmx/GetTeamMembers"


def ajax_request():
  '''
  Get the data from the web. This tries to immitate the 'function getTeamMembers() {' in the 
  source code of the website here: view-source:https://secure.e2rm.com/registrant/TeamFundraisingPage.aspx?teamID=738302&langPref=en-CA
  return: 
    :list a list containing dictionaries of donations. 
          example: 
          [{'name': 'Johanna Nicoletta', 'isTeamCaptain': 'True', 'amount': '$277.38', 'facebookId': '1633682560', 'pageUrl': 'https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3697209&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA'}, {'name': 'Ericsson Activities', 'isTeamCaptain': 'False', 'amount': '$194.00', 'facebookId': '', 'pageUrl': 'https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3877056&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA'}, {'name': 'Alireza Mirzaee', 'isTeamCaptain': 'False', 'amount': '$25.00', 'facebookId': '', 'pageUrl': 'https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3869108&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA'}, {'name': 'Hossein Seyedmehdi', 'isTeamCaptain': 'False', 'amount': '$0.00', 'facebookId': '', 'pageUrl': 'https://secure.e2rm.com/registrant/FundraisingPage.aspx?registrationID=3855399&langPref=en-CA&Referrer=https%3a%2f%2fsecure.e2rm.com%2fregistrant%2fsearch.aspx%3feventid%3d210107%26langpref%3den-CA'}]

  '''
    
  session = Session()
  
  # to get the payload, use the Chrome Developer Mode (alt+command+I in Mac) >> Network >> XHR >> GetTeamMembers >> Headers >> Request Payload  
  payload = json.dumps({'teamID':738302,
                        'languageCode':'en-CA',
                        'sourceReferrerUrl':'https://secure.e2rm.com/registrant/search.aspx?eventid=210107&langpref=en-CA',
                        'anonymousText':'Anonymous',
                        'isOrderByAmount':'true'})
  
  response = session.post(url = url_ajax_request, data = payload, headers={'content-type':'application/json'})
  
  response_dict = response.json()
  donation_list = json.loads(response_dict['d'])
  return donation_list

if __name__ == "__main__": 
  r = ajax_request()
  print(r)
  print(r[0]['name'])
  
  
  

