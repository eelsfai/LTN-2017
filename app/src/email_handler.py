'''
Created on Aug 30, 2017

@author: Hossein
'''

import os 

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'ltn.ericsson@gmail.com'

def get_data_path():
  '''
  Gets the path of the "data" directory, which will have subdirectories
  for different data files.

  returns:
    :str : Absolute path to the "data" directory.
  '''
  script_dirname = os.path.dirname(os.path.abspath(__file__))
  return os.path.join(script_dirname, '..', 'data')

def get_raw_data_path():
  '''
  gets the absolute path to the folder for the raw data
  returns: 
    :str : the absolute path to the data folder, e.g., /app/data/raw_data/
  ''' 
  return os.path.join(get_data_path(), 'raw_data')

def get_visual_data_path():
  '''
  gets the absolute path to the folder that conains the visualization data
  returns: 
    :str : the absolute path to the visualized data folder, e.g., /app/data/visual_data/
  ''' 
  return os.path.join(get_data_path(), 'visual_data')

def get_files_to_be_sent(data_dir):
  '''
  Obtains a listing of the files inside the directory specified by data_dir,
  filters out unwanted files and returns a list of the file paths.

    :str : List of paths of files in data_dir.
  '''
  files_in_dir = os.listdir(data_dir)
  files_to_be_sent = []

  for file_in_dir in files_in_dir:
    if file_in_dir.startswith("."):
      # Exclude "hidden" files.
      continue
    elif file_in_dir.endswith(".py"):
      # Exclude Python source code.
      continue

    files_to_be_sent.append(os.path.join(data_dir, file_in_dir))

  return files_to_be_sent

def send_email(data_dir, recipients=[ MAIL_USERNAME ]):
  ''' 
  19.1.14. email: Examples
  https://docs.python.org/3.4/library/email-examples.html
  '''

  import smtplib
  from os.path import basename
  from email.mime.application import MIMEApplication
  from email.mime.multipart import MIMEMultipart
  from email.mime.text import MIMEText 

  if 'MAIL_PASSWORD' not in os.environ:
    raise Exception("Could not find the \"MAIL_PASSWORD\" environment variable.")

  mail_password = os.environ['MAIL_PASSWORD']

  msg = MIMEMultipart()
  msg['From'] = MAIL_USERNAME
  msg['To'] = ', '.join(recipients)
  msg['Subject'] = "Test email for LTN"
   
  body = "The Email Body"
  msg.attach(MIMEText(body, 'plain'))

  for data_file_name in get_files_to_be_sent(data_dir):
    # Attach the files
    with open(data_file_name, "rb") as fil:
      part = MIMEApplication(
          fil.read(),
          Name = basename(data_file_name) )

    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(data_file_name)
    msg.attach(part)

  text = msg.as_string()
   
  server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
  server.starttls()
  server.login(MAIL_USERNAME, mail_password)
  server.sendmail(MAIL_USERNAME, recipients, text)
  server.quit()
