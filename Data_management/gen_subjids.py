"""
Created on Aug. 24, 2016
Upated on Aug. 26, 2016

Generate array with subjids to be passed onto datagrabber
NOTE: Directories are all hard coded
      Change 'Desktop/Test/' to appropriate folder as needed 
      (ie. 'EpilepsyDatabase/')
"""

########
# Import
########
import os, getpass # Directory & user library
from nipype import IdentityInterface, Node

# Global Variables
user = getpass.getuser() # Grabs username of user currently logged on
base_dir = '/home/ROBARTS/' + user + '/Desktop/Test/'

#################
# Content sorting
#################
listids = os.listdir(base_dir) # Store the contents of the path
sort_listids = sorted(listids) # Sort contents alphabetically

# Array to store subject ids
subjid = []

for subj in range(len(sort_listids)):
    if "EPI_" in sort_listids[subj]:
        subjid.append(sort_listids[subj])
        
##############################
# Iterable list of subject ids
##############################
node_subjid = Node(IdentityInterface(fields=['subject_id']),name="subjid")
node_subjid.iterables = [('subject_id', subjid)]
