'''
Created on Sep 9, 2017

@author: Hossein
'''

import utils
import os
import json
import datetime
import copy

def str2date(date_str):
  '''
  convert YYYY-MM-DD to datetime.date
  '''
  splitted_date = date_str.split('-')
  # convert to int 
  d = [int(s) for s in splitted_date]
  return datetime.date(d[0], d[1], d[2])
 
def get_sum_donations(team_members):
  '''
  computes the sum_donations of donations for all team members
  input 
    :dict : a dictionary of team members
  output
    :float : sum of donations 
  '''
  sum_donations = 0 
  for member_info in team_members:
    # get the amount field and remove dollar sign  
    amount = member_info['amount'].replace('$', '')
    sum_donations += float(amount)
  return sum_donations

def get_highest_donation(supporters_data, window_days):
  '''
  return the highest donation within the past number of days 
  input: 
    :list : a ledger containing supporter's data ['2017-09-01': {}, ...]
    :int : a window size indicates how many days it comparison  goes back. 
            For instance, if window_days == 1, the function gets the highest 
            donation today; if window_days == 7, the function will
            return the highest donation within the past week.
  return: 
    :dict : {'supporter_name': a_supporter_name, 'amount': a_dollar_amount, 
            'supportee': a_team_member, 'message': a_message }
  '''
  # get the day before the window day
  cutoff_day = datetime.date.today() - datetime.timedelta(days = window_days)
  days_before_cutoff = [day for day in supporters_data if str2date(day) < cutoff_day]
  # Find the day 'YYYY-MM-DD' right before the window day
  day_before_cutoff = ''
  if len(days_before_cutoff) > 0: 
    day_before_cutoff = max(days_before_cutoff) #the day before cut off

  # get the supporters on the day right before the beginning of the window
  supporters_before_cutoff = []
  if day_before_cutoff in supporters_data: 
    supp_data = supporters_data[day_before_cutoff]
    for member in supp_data: 
      for supporter in supp_data[member]: 
        supp = copy.copy(supporter) #E.g., supp = {'time': 'Jul 19, 2017 12:00 AM', 'message': '', 'amount_dollar': '229.41', 'supporter_name': 'ericssoncommunity'}
        supp['team_member'] = member 
        supporters_before_cutoff.append(supp)     
   
  # get the supporters on the last day of the ledger   
  last_day = max(supporters_data)
  supporters_within_window = []
  supp_data = supporters_data[last_day]
  for member in supp_data: 
    for supporter in supp_data[member]: 
      #print("supporter = " + json.dumps(supporter))
      supp = copy.copy(supporter)
      supp['team_member'] = member
      # Subtract the supporters before the window day from the supporters 
      # on the last day to get the donations within the days determined by 
      # the window_days. But since these are lists of dictionaries, the 
      # subtraction is not straight forward. 
      if supp not in supporters_before_cutoff: 
        supporters_within_window.append(supp)
  # find the highest donor:
  if len(supporters_within_window) > 0:
    # remove the dollar sign and compare all donation amounts to find the max
    highest_donation = max(supporters_within_window, key = lambda x: float(x['amount_dollar'].replace('$', '')))
    return highest_donation

def get_donation_by_division(team_data, divisions, member_division_mapping):
  return

if __name__ == "__main__":
  # tests
  dstr = "2017-09-01"
  print("date str of {} is {}.".format(dstr, str2date(dstr)))
  #
  fname = os.path.join(utils.get_raw_data_path(), 'member_data.txt')
  with open(fname) as f: 
    f_data = f.read()
    member_data = json.loads(f_data)
  for k in member_data: 
    member_data_snapshot = member_data[k]
    #print(json.dumps(member_data_snapshot, indent=4))
    print("sum donation is {} dollar".format(get_sum_donations(member_data_snapshot)))
    break
  
  fname2 = os.path.join(utils.get_raw_data_path(), 'supporters_data.txt')
  with open(fname2) as f: 
    f_data = f.read()
    supporters_data = json.loads(f_data)
  print()
  print("highest donation for past two days is {}.".format(get_highest_donation(supporters_data, 2))) 
  print("highest donation during past week is {}.".format(get_highest_donation(supporters_data, 7))) 
  print("highest donation overall is {}.".format(get_highest_donation(supporters_data, 1000))) 

  print()
  


