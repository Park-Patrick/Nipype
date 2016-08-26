"""
Created on Aug. 25, 2016
Upated on Aug. 26, 2016

Datagrabber for DWI files (dwi.nii.gz, dwi.bval, dwi.bvec)
NOTE: Directories are all hard coded
      Change work_dir to appropriate folder as needed 
      (ie. 'EpilepsyDatabase/')
      
      Temp folder dwi_grabber is generated in base directory
      
NA: TEST WITH PROPER WORKFLOW
"""
########
# Import
########
import getpass # Import getpass library to pull current user
import gen_subjids # Imports list of subject ids 
from nipype import IdentityInterface, Node, SelectFiles, Workflow

# Global variables
user = getpass.getuser() # Grabs current user name
base_dir = '/home/ROBARTS/' + user + '/Desktop/'
work_dir = '/home/ROBARTS/' + user + '/Desktop/Test/'

##############################
# Iterable list of subject ids
##############################
node_subjid = Node(IdentityInterface(fields=['subject_id']),name="subjid")
node_subjid.iterables = [('subject_id', gen_subjids.subjid)]

# DWI template - files previously imported
templates={'dwi': work_dir + "{subject_id}/dti/uncorrected/dwi.nii.gz",
           'bval': work_dir + "{subject_id}/dti/uncorrected/dwi.bval",
           'bvec': work_dir + "{subject_id}/dti/uncorrected/dwi.bvec"}
           
# DWIGrabber (SelectFiles) node creation
node_dwiSelect = Node(SelectFiles(templates), name="SelectFiles")
node_dwiSelect.base_dir = base_dir
node_dwiSelect.inputs.base_directory = work_dir
node_dwiSelect.inputs.sort_filelist = False

############################
# Workflow to grab datafiles
############################
dwiGrab = Workflow(name='dwi_grabber')
dwiGrab.base_dir = base_dir

# Add nodes
dwiGrab.add_nodes([node_subjid])
dwiGrab.add_nodes([node_dwiSelect])

# Connect nodes
dwiGrab.connect(node_subjid, 'subject_id', node_dwiSelect, 'subject_id')