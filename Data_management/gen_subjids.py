"""
Created on Aug. 24, 2016
Upated on Aug. 25, 2016

Generate array with subjids to be passed onto datagrabber
NOTE: Directories are all hard coded
      Change 'Desktop/Test/' to appropriate folder as needed 
      (ie. 'EpilepsyDatabase/')
"""

########
# Import
########
import os, getpass # Directory & user library

# Global Variables
user = getpass.getuser() # Grabs username of user currently logged on
base_dir = '/home/ROBARTS/' + user + '/Desktop/Test/'

#################
# Content sorting
#################
listids = os.listdir(base_dir) # Store the contents of the path
sort_listids = sorted(listids) # Sort contents alphabetically

# Array to store subject ids
subjids = []

for subj in range(len(sort_listids)):
    if "EPI_" in sort_listids[subj]:
        subjids.append(sort_listids[subj])
