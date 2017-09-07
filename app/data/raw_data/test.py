'''
Created on Sep 7, 2017

@author: Hossein
'''

import json

file_names = ['divisions_ericsson.txt', 'division_members_mapping.txt']

for fname in file_names: 
  with open(fname) as f: 
    c = f.read()
    print(c)
    d = json.loads(c)
  
  with open(fname, 'w') as f: 
    f.write(json.dumps(d, indent=4))
  
print("Done!")