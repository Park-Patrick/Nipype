"""
Created on Aug. 25, 2016
Upated on Aug. 26, 2016

Datagrabber for T1 file (t1.nii.gz)
NOTE: Directories are all hard coded
      Change work_dir to appropriate folder as needed 
      (ie. 'EpilepsyDatabase/')
      
      Temp folder t1_grabber is generated in base directory
      
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
templates={'t1': work_dir + "{subject_id}/t1/t1.nii.gz"}
           
# DWIGrabber (SelectFiles) node creation
node_t1Select = Node(SelectFiles(templates), name="SelectFiles")
node_t1Select.base_dir = base_dir
node_t1Select.inputs.base_directory = work_dir
node_t1Select.inputs.sort_filelist = False

############################
# Workflow to grab datafiles
############################
t1Grab = Workflow(name='t1_grabber')
t1Grab.base_dir = base_dir

# Add nodes
t1Grab.add_nodes([node_subjid])
t1Grab.add_nodes([node_t1Select])

# Connect nodes
t1Grab.connect(node_subjid, 'subject_id', node_t1Select, 'subject_id')