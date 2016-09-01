"""
Created on Aug. 25, 2016
Upated on Aug. 31, 2016

Datagrabber for DWI files (dwi.nii.gz, dwi.bval, dwi.bvec)
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
# DWIGrabber
############
# Template
templates={'dwi': work_dir + "{subject_id}/dti/uncorrected/dwi.nii.gz",
           'bvec': work_dir + "{subject_id}/dti/uncorrected/dwi.bvec",           
           'bval': work_dir + "{subject_id}/dti/uncorrected/dwi.bval",
           }

# Node
node_dwiSelect = pe.Node(SelectFiles(templates), name="SelectFiles")
node_dwiSelect.base_dir = base_dir
node_dwiSelect.inputs.base_directory = work_dir
node_dwiSelect.inputs.sort_filelist = False
