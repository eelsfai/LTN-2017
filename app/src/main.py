'''
Created on Aug 29, 2017

@author: Hossein
'''
import argparse
import os 
from email_handler import send_email
import utils # import get_raw_data_path, get_visual_data_path
from tqdm import tqdm
import scraping
import analytics
import visualizer

FILE_NAME_MEMBERS = 'member_data.txt'
FILE_NAME_SUPPORTERS = 'supporters_data.txt'

if __name__ == "__main__": 
  parser = argparse.ArgumentParser(description='Data analytics and Visualization for LightTheNight (DaViL)')
  parser.add_argument('--no-email', dest='send_email', default=True, action='store_false')

  args = parser.parse_args()

  # get the absolute path to the data files
  team_data_file = os.path.join(utils.get_raw_data_path(), FILE_NAME_MEMBERS)
  supporters_data_file = os.path.join(utils.get_raw_data_path(), FILE_NAME_SUPPORTERS)

  
  #
  # Scrape the web
  #
  team_members = scraping.get_team_members()
  # Update the ledger file with new team member data
  team_ledger = utils.load_from_file(team_data_file)
  scraping.update_ledger(team_ledger, team_members)
  utils.save_to_file(team_data_file, team_ledger)
  # Get each team member's page showing the supporters and detailed amount of donations
  print("Getting all the pages for team members...")
  all_supporters = {}
  for member in tqdm(team_members): 
    p_url = member['pageUrl']
    name = member['name']
    all_supporters[name] = scraping.parse_member_page(scraping.get_member_page(p_url))
  # Update the supporter's ledger in the files
  supporters_ledger = utils.load_from_file(supporters_data_file)
  scraping.update_ledger(supporters_ledger, all_supporters)
  utils.save_to_file(supporters_data_file, supporters_ledger)

  #
  # Perform analytics 
  #
  print("Performing analytics...")
  msg = 'Auto Generated email -- Do not reply.\n ------- \n\n'
  msg += 'Thanks to LTN top supporters:\n'
  window_days_list = [("Yesterday", 2), ("Last 7 days", 7), ("Last 30 days", 30), ("Overall in 2017", 365)]
  last_hd = None
  for window_days in window_days_list:
    highest_donation = analytics.get_highest_donation(supporters_ledger, window_days[1])
    if highest_donation and highest_donation != last_hd:
      last_hd = highest_donation
      msg += "\t" + window_days[0] + ":\n" 
      msg += '\t\t{} donated ${} to {}.\n'\
              .format(highest_donation['supporter_name'], highest_donation['amount_dollar'],
                      highest_donation['team_member'])
      if highest_donation['message']:
        msg += '\t\t"{}"\n'.format(highest_donation['message'])
  #print(msg)
  # get data for donations per divisions 
  fname = os.path.join(utils.get_raw_data_path(), 'members_divisions.txt')
  members_divisions = utils.load_from_file(fname)
  fname = os.path.join(utils.get_raw_data_path(), 'ericsson_divisions.txt')
  ericsson_divisions = utils.load_from_file(fname)
  dbd = analytics.get_donation_by_division(team_ledger, members_divisions)
  # Historical donation 
  doantions_over_time = analytics.get_historical_donaitons(team_ledger)
  # Get division of all team members 
  mem_div = analytics.get_all_members_division(team_ledger, members_divisions)
  fname = os.path.join(utils.get_admin_data_path(), 'members_divisions.txt')
  utils.save_to_file(fname, mem_div)
  
  #
  # Visualization
  #
  file_name = os.path.join(utils.get_visual_data_path(), 'divisions.png')
  visualizer.generate_bar_chart(dbd,  file_name) 
  #
  file_name = os.path.join(utils.get_visual_data_path(), 'time_series.png')
  visualizer.generate_time_series(doantions_over_time, file_name)
 
  #
  # Sending email
  #
  if args.send_email:
    print("Sending e-mail...")
    send_email(utils.get_raw_data_path(), body="Auto generated email.")
    send_email(utils.get_visual_data_path(), subject = "Today's LTN stats for site monitors.", body=msg)
    send_email(utils.get_admin_data_path(), subject = "LTN admin data.", body="Auto generated email...")


  print("Done!")
