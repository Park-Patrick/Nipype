"""
Created on Aug. 25, 2016
Upated on Aug. 31, 2016

Datagrabber for T1 file (t1.nii.gz)
NOTE: Directories are all hard coded
      Change work_dir to appropriate folder as needed 
      (ie. 'EpilepsyDatabase/')
"""
########
# Import
########
import getpass # Import getpass library to pull current user
import nipype.pipeline as pe
from nipype import SelectFiles

# Pathing
user = getpass.getuser() # Grabs current user name
base_dir = '/home/ROBARTS/' + user + '/Desktop/'
work_dir = '/home/ROBARTS/' + user + '/Desktop/Test/'

############
# T1Grabber
############
# Template
templates={'t1': work_dir + "{subject_id}/t1/t1.nii.gz"}

# Node
node_t1Select = pe.Node(SelectFiles(templates), name="SelectFiles")
node_t1Select.base_dir = base_dir
node_t1Select.inputs.base_directory = work_dir
node_t1Select.inputs.sort_filelist = False
