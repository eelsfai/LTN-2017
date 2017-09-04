'''
Created on Aug 30, 2017

@author: Hossein
'''

import os 

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'ltn.ericsson@gmail.com'

MAIL_PASSWORD = ''
if 'MAIL_PASSWORD' in os.environ: 
  MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
  

def get_raw_data_path():
  '''
  gets the absolute path to the folder for the raw data
  returns: 
    :str : the absolute path to the data folder, e.g., /app/data/raw_data/
  ''' 
  script_dirname, script_filename = os.path.split(os.path.abspath(__file__))
  path_to_data = os.path.join(script_dirname, '../data/raw_data')
  return path_to_data

def get_visual_data_path():
  '''
  gets the absolute path to the folder that conains the visualization data
  returns: 
    :str : the absolute path to the visualized data folder, e.g., /app/data/visual_data/
  ''' 
  script_dirname, script_filename = os.path.split(os.path.abspath(__file__))
  path_to_data = os.path.join(script_dirname, '../data/visual_data')
  return path_to_data

def send_email(data_file_name, to_addr):
  ''' 
  19.1.14. email: Examples
  https://docs.python.org/3.4/library/email-examples.html
  
  '''

  import smtplib
  from os.path import basename
  from email.mime.application import MIMEApplication
  from email.mime.multipart import MIMEMultipart
  from email.mime.text import MIMEText 
 
  from_addr = MAIL_USERNAME
  #to_addr = ["hossein.seyedmehdi@gmail.com", "hossein.seyedmehdi@ericsson.com"]
  to_addr_str = ''
  for addr in to_addr: 
    to_addr_str += addr + ', '
  msg = MIMEMultipart()
  msg['From'] = from_addr
  msg['To'] = to_addr_str
  msg['Subject'] = "Test email for LTN"
   
  body = "The Email Body"
  msg.attach(MIMEText(body, 'plain'))
  
  #Attach the file 
  with open(data_file_name, "rb") as fil:
    part = MIMEApplication(
        fil.read(),
        Name = basename(data_file_name) )
  # After the file is closed
  part['Content-Disposition'] = 'attachment; filename="%s"' % basename(data_file_name)
  msg.attach(part)
   
  server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
  server.starttls()
  server.login(from_addr, MAIL_PASSWORD)
  text = msg.as_string()
  for addr in to_addr:
    server.sendmail(from_addr, addr, text)
  server.quit()
  
  return
  
