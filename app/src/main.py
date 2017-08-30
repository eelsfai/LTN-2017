'''
Created on Aug 29, 2017

@author: Hossein
'''


from requests import Session


def get_data_from_web():
  '''
  Get the data from the web. This tries to immitate the 'function getTeamMembers() {' in the 
  source code of the website here: view-source:https://secure.e2rm.com/registrant/TeamFundraisingPage.aspx?teamID=738302&langPref=en-CA 
  '''
  name_money_dict = {}
  session = Session()
  
  '''
  var teamId = parseInt($teamListContainer.attr("data-team-id"));
  var languageCode = $teamListContainer.attr("data-language-code");
  var sourceReferrerUrl = $teamListContainer.attr("data-source-referrer");
  var anonymousText = $teamListContainer.find(".anonymous-team-member").text();
  var isOrderByAmount = $teamListContainer.attr("data-order-by-amount") == "True";
  '''
  
  team_page_url = "https://secure.e2rm.com/registrant/TeamFundraisingPage.aspx?teamID=738302&langPref=en-CA"
  ajax_call_url = "https://secure.e2rm.com/registrant/WebServices/RegistrantWebService.asmx/GetTeamMembers"
  teamId = "738302"
  languageCode = "en-CA"
  sourceReferrerUrl = "https://secure.e2rm.com/registrant/search.aspx?eventid=210107&langpref=en-CA"
  anonymousText = "Anonymous"
  isOrderByAmount = "true"
  
  print(session.cookies.get_dict())
  r = session.get(team_page_url)
  print(r.headers)
  print(session.cookies.get_dict())
  
  return 

  response = session.post(
    url = ajax_call_url,
    data = {'teamID': teamId, 
            'languageCode': languageCode, 
            'sourceReferrerUrl': sourceReferrerUrl, 
            'anonymousText': anonymousText, 
            'isOrderByAmount': isOrderByAmount}, 
    headers = r.headers)
   
  print(response.text)
  
  return response 

if __name__ == "__main__": 
  response = get_data_from_web()
  #print(response)
  
  
  
#ASP.NET_SessionId=kfage2wf4qnazbeh30g2dnt2; BIGipServersecure.e2rm.com=1130647562.20480.0000
#kfage2wf4qnazbeh30g2dnt2
#1130647562.20480.0000
  
  
# /registrant/TeamFundraisingPage.aspx
  
  