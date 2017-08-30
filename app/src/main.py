'''
Created on Aug 29, 2017

@author: Hossein
'''

from selenium import webdriver

url_main_team_page = "https://secure.e2rm.com/registrant/TeamFundraisingPage.aspx?teamID=738302&langPref=en-CA"
url_ajax_request = "https://secure.e2rm.com/registrant/WebServices/RegistrantWebService.asmx/GetTeamMembers"


def ajax_request():
  '''
  Get the data from the web. This tries to immitate the 'function getTeamMembers() {' in the 
  source code of the website here: view-source:https://secure.e2rm.com/registrant/TeamFundraisingPage.aspx?teamID=738302&langPref=en-CA 
  '''
  
  '''
  var teamId = parseInt($teamListContainer.attr("data-team-id"));
  var languageCode = $teamListContainer.attr("data-language-code");
  var sourceReferrerUrl = $teamListContainer.attr("data-source-referrer");
  var anonymousText = $teamListContainer.find(".anonymous-team-member").text();
  var isOrderByAmount = $teamListContainer.attr("data-order-by-amount") == "True";
  '''

  from requests import Session
  import json
  
  url_main_team_page = "https://secure.e2rm.com/registrant/TeamFundraisingPage.aspx?teamID=738302&langPref=en-CA"
  url_ajax_request = "https://secure.e2rm.com/registrant/WebServices/RegistrantWebService.asmx/GetTeamMembers"
  
  session = Session()
  
  #print(session.cookies.get_dict())
  session.get(url_main_team_page)
  #print(session.cookies.get_dict())
  
  payload = json.dumps({'teamID':738302,
                        'languageCode':'en-CA',
                        'sourceReferrerUrl':'https://secure.e2rm.com/registrant/search.aspx?eventid=210107&langpref=en-CA',
                        'anonymousText':'Anonymous',
                        'isOrderByAmount':'true'})
  
  response = session.post(url = url_ajax_request, data = payload)
   
  print(response.text)
  
  return response 

def headless_request():
  driver = webdriver.PhantomJS()
  driver.get(url_main_team_page)
  r = driver.page_source()
  r.find("Johanna") 

if __name__ == "__main__": 
  #headless_request()
  ajax_request()


#ASP.NET_SessionId=kfage2wf4qnazbeh30g2dnt2; BIGipServersecure.e2rm.com=1130647562.20480.0000
#kfage2wf4qnazbeh30g2dnt2
#1130647562.20480.0000
  
  
# /registrant/TeamFundraisingPage.aspx
  
  