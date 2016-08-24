##################
# Import modules #
##################

from nipype.interfaces.base import(
    TraitedSpec,
    CommandLineInputSpec,
    CommandLine,
    File,
    traits
)
import nipype.interfaces.ants as ants
import nipype.interfaces.fsl as fsl
import nipype.interfaces.freesurfer as fsurfer

import wrapper2_reg_aladin as w_reg_aladin
import wrapper_reg_f3d as w_reg_f3d
import wrapper_reg_jacobian as w_reg_jacobian

#import nipype engine
import nipype.pipeline.engine as pe

###########################
# Set file name variables #
###########################

#root directory
root_dir = '/home/ROBARTS/ppark/Documents/park_test_geo_dbm/nipype/EPI_P021/'

#input files (not generated within pipeline)
despot1 = 'despot1_tr90_fa18.nii.gz'
despot1_mask = 'BrainMask.nii.gz'

highres = 'MPRAGE_std_N4.nii.gz'
highres_bet = 'MPRAGE_std_N4_bet.nii.gz'
highres_mask = 'MPRAGE_std_N4_bet_BrainMask.nii.gz'

#output file names
despot1_nuc = 'despot1_tr90_fa18_nuc.nii.gz'
despot1_nuc_masked = 'despot1_tr90_fa18_nuc_masked.nii.gz'

resampled_despot1 = 'despot1_05mm.nii.gz'
resampled_despot1_mask = 'despot1_05mm_BrainMask.nii.gz'

resampled_highres = 'MPRAGE_std_N4_05mm.nii.gz'
resampled_highres_bet = 'MPRAGE_std_N4_bet_05mm.nii.gz'
resampled_highres_mask = 'MPRAGE_std_N4_05mm_BrainMask.nii.gz'

rigid_xfm = '7T_to_3T_rigid_xfm.txt'
rigid_nii = '7T_to_3T_rigid.nii'

affine_xfm = '7T_to_3T_affine_xfm.txt'
affine_nii = '7T_to_3T_affine.nii'

nlin_cpp = '7T_to_3T_nlin_cpp.nii'
nlin_nii = '7T_to_3T_nlin.nii'

log_jacobian = '7T_to_3T_log_jacobian.nii'
mat_jacobian = '7T_to_3T_mat_jacobian.nii'
jacobian = '7T_to_3T_jacobian.nii'

resampleVS = (0.5, 0.5, 0.5)

################
# Create Nodes #
################

# wraps command N4BiasFieldCorrection #

node_N4BiasFieldCorrection = pe.Node(interface=ants.N4BiasFieldCorrection(), name='node_N4BiasFieldCorrection')
node_N4BiasFieldCorrection.inputs.input_image = root_dir + despot1
node_N4BiasFieldCorrection.inputs.output_image = root_dir + despot1_nuc
#default save_bias set to false. Output is output_image
#print node_N4BiasFieldCorrection.interface.cmdline

# wraps command fslmaths with -mul flag #

node_fslmath_multiply = pe.Node(interface=fsl.BinaryMaths(), name = 'node_fslmath_multiply')
# uncomment for individual node testing #
#node_fslmath_multiply.inputs.in_file = root_dir + despot1_nuc
#node_fslmath_multiply.inputs.in_file = node_N4BiasFieldCorrection.inputs.output_image
node_fslmath_multiply.inputs.operand_file = root_dir + despot1_mask
node_fslmath_multiply.inputs.operation = "mul"
node_fslmath_multiply.inputs.out_file = root_dir + despot1_nuc_masked
#print node_fslmath_multiply.interface.cmdline

# wraps command fslmaths with -bin flag #

node_fslmath_binarize = pe.Node(interface=fsl.UnaryMaths(), name = 'node_fslmath_binarize')
node_fslmath_binarize.inputs.operation = 'bin'
node_fslmath_binarize.inputs.in_file = root_dir + highres_bet
node_fslmath_binarize.inputs.out_file = root_dir + highres_mask
#print node_fslmath_binarize.interface.cmdline

# wraps command mri_convert #
# mRs = mri_Resample

#highres
node_mRs = pe.Node(interface=fsurfer.Resample(), name = 'node_mRs')
node_mRs.inputs.voxel_size = resampleVS
node_mRs.inputs.in_file = root_dir + highres
node_mRs.inputs.resampled_file = root_dir + resampled_highres
#print node_mRs.interface.cmdline

#highres_bet
node_mRs_highres_bet = pe.Node(interface=fsurfer.Resample(), name = 'node_mRs_highres_bet')
node_mRs_highres_bet.inputs.voxel_size = resampleVS
node_mRs_highres_bet.inputs.in_file = root_dir + highres_bet
node_mRs_highres_bet.inputs.resampled_file = root_dir + resampled_highres_bet
#print node_mRs_highres_bet.interface.cmdline

#highres_mask
node_mRs_highres_mask = pe.Node(interface=fsurfer.Resample(), name = 'node_mRs_highres_mask')
node_mRs_highres_mask.inputs.voxel_size = resampleVS
node_mRs_highres_mask.inputs.in_file = root_dir + highres_mask
node_mRs_highres_mask.inputs.resampled_file = root_dir + resampled_highres_mask
#print node_mRs_highres_mask.interface.cmdline

#despot1
node_mRs_despot1 = pe.Node(interface=fsurfer.Resample(), name = 'node_mRs_despot1')
node_mRs_despot1.inputs.voxel_size = resampleVS
node_mRs_despot1.inputs.in_file = root_dir + despot1_nuc_masked
node_mRs_despot1.inputs.resampled_file = root_dir + resampled_despot1
#print node_mRs_despot1.interface.cmdline

#despot1_mask
node_mRs_despot1_mask = pe.Node(interface=fsurfer.Resample(), name = 'node_mRs_despot1_mask')
node_mRs_despot1_mask.inputs.voxel_size = resampleVS
node_mRs_despot1_mask.inputs.in_file = root_dir + despot1_mask
node_mRs_despot1_mask.inputs.resampled_file = root_dir + resampled_despot1_mask
#print node_mRs_despot1_mask.interface.cmdline

#niftyReg rigid aladin
node_reg_aladin = pe.Node(interface = w_reg_aladin.reg_aladin(), name = 'node_reg_aladin')
node_reg_aladin.inputs.reference_img = root_dir + resampled_despot1
node_reg_aladin.inputs.floating_img = root_dir + resampled_highres_bet
node_reg_aladin.inputs.option_rigOnly = True
node_reg_aladin.inputs.option_affine = root_dir + rigid_xfm
node_reg_aladin.inputs.resampled_image = root_dir + rigid_nii
#print node_reg_aladin.interface.cmdline

#niftyReg non rigid aladin
node_reg_aladin2 = pe.Node(interface=w_reg_aladin.reg_aladin(), name = 'node_reg_aladin2')
node_reg_aladin2.inputs.reference_img = root_dir + resampled_despot1
node_reg_aladin2.inputs.floating_img = root_dir + resampled_highres_bet
node_reg_aladin2.inputs.input_affine_trans = root_dir + rigid_xfm
node_reg_aladin2.inputs.option_affine = root_dir + affine_xfm
node_reg_aladin2.inputs.resampled_image = root_dir + affine_nii
#print node_reg_aladin2.interface.cmdline

#niftyReg f3d
node_reg_f3d = pe.Node(interface=w_reg_f3d.reg_f3d(), name = 'node_reg_f3d')
node_reg_f3d.inputs.reference_img = root_dir + resampled_despot1
node_reg_f3d.inputs.floating_img = root_dir + resampled_highres_bet
node_reg_f3d.inputs.option_affine = root_dir + affine_xfm
node_reg_f3d.inputs.control_point_grid = root_dir + nlin_cpp
node_reg_f3d.inputs.resampled_img = root_dir + nlin_nii
#print node_reg_f3d.interface.cmdline

#niftyReg jacobian Log
node_jacobian_log = pe.Node(interface=w_reg_jacobian.reg_jacobian(), name = 'node_jacobian_log')
node_jacobian_log.inputs.reference_img = root_dir + resampled_despot1
node_jacobian_log.inputs.control_point_grid = root_dir + nlin_cpp
node_jacobian_log.inputs.option_affine = root_dir + affine_xfm    
node_jacobian_log.inputs.jacobianLog = root_dir + log_jacobian
#print node_jacobian_log.interface.cmdline

#niftyReg jacobian matrix
node_jacobian_matrix = pe.Node(interface=w_reg_jacobian.reg_jacobian(), name = 'node_jacobian_matrix')
node_jacobian_matrix.inputs.reference_img = root_dir + resampled_despot1
node_jacobian_matrix.inputs.control_point_grid = root_dir + nlin_cpp
node_jacobian_matrix.inputs.option_affine = root_dir + affine_xfm    
node_jacobian_matrix.inputs.jacobianMatrix = root_dir + mat_jacobian
#print node_jacobian_matrix.interface.cmdline

#niftyReg jacobian determinant
node_jacobian_dtm = pe.Node(interface=w_reg_jacobian.reg_jacobian(), name = 'node_jacobian_dtm')
node_jacobian_log.inputs.reference_img = root_dir + resampled_despot1
node_jacobian_log.inputs.control_point_grid = root_dir + nlin_cpp
node_jacobian_log.inputs.option_affine = root_dir + affine_xfm    
node_jacobian_log.inputs.jacobianDeterminant = root_dir + jacobian
#print node_jacobian_log.interface.cmdline

####################
# Create workflows #
####################
#TODO: break pipeline down into sub-workflows

test_geo_workflow2 = pe.Workflow(name='test_geo_workflow2')
test_geo_workflow2.base_dir = '.'

#############
# Add nodes #
#############
#TODO: can be simplified to one line per sub-workflow


test_geo_workflow2.add_nodes([node_fslmath_binarize])
test_geo_workflow2.add_nodes([node_fslmath_multiply])
test_geo_workflow2.add_nodes([node_jacobian_dtm])
test_geo_workflow2.add_nodes([node_jacobian_log])
test_geo_workflow2.add_nodes([node_jacobian_matrix])
test_geo_workflow2.add_nodes([node_mRs])
test_geo_workflow2.add_nodes([node_mRs_despot1])
test_geo_workflow2.add_nodes([node_mRs_despot1_mask])
test_geo_workflow2.add_nodes([node_mRs_highres_bet])
test_geo_workflow2.add_nodes([node_mRs_highres_mask])
test_geo_workflow2.add_nodes([node_N4BiasFieldCorrection])
test_geo_workflow2.add_nodes([node_reg_aladin])
test_geo_workflow2.add_nodes([node_reg_aladin2])
test_geo_workflow2.add_nodes([node_reg_f3d])


#################
# Connect nodes #
#################
#TODO: can be simplified to one line per sub-workflow

test_geo_workflow2.connect(node_N4BiasFieldCorrection, 'output_image', node_fslmath_multiply, 'in_file')
test_geo_workflow2.connect(node_fslmath_multiply, 'out_file', node_mRs_despot1, 'in_file')
test_geo_workflow2.connect(node_mRs_highres_bet, 'resampled_file', node_reg_aladin, 'floating_img')
test_geo_workflow2.connect(node_mRs_highres_bet, 'resampled_file', node_reg_aladin2, 'floating_img')
test_geo_workflow2.connect(node_reg_aladin, 'output_affine_transformation', node_reg_aladin2, 'input_affine_trans')
#reference images
test_geo_workflow2.connect(node_mRs_despot1, 'resampled_file', node_reg_aladin, 'reference_img')
test_geo_workflow2.connect(node_mRs_despot1, 'resampled_file', node_reg_aladin2, 'reference_img')
test_geo_workflow2.connect(node_mRs_despot1, 'resampled_file', node_reg_f3d, 'reference_img')
test_geo_workflow2.connect(node_mRs_despot1, 'resampled_file', node_jacobian_dtm, 'reference_img')
test_geo_workflow2.connect(node_mRs_despot1, 'resampled_file', node_jacobian_log, 'reference_img')
test_geo_workflow2.connect(node_mRs_despot1, 'resampled_file', node_jacobian_matrix, 'reference_img')

test_geo_workflow2.connect(node_mRs_highres_bet, 'resampled_file', node_reg_f3d, 'floating_img')
test_geo_workflow2.connect(node_reg_aladin2, 'output_affine_transformation', node_reg_f3d, 'option_affine')

test_geo_workflow2.connect(node_reg_f3d, 'outfile_cpp', node_jacobian_log, 'control_point_grid')
test_geo_workflow2.connect(node_reg_f3d, 'outfile_cpp', node_jacobian_matrix, 'control_point_grid')
test_geo_workflow2.connect(node_reg_f3d, 'outfile_cpp', node_jacobian_dtm, 'control_point_grid')

test_geo_workflow2.connect(node_reg_aladin2, 'output_affine_transformation', node_jacobian_log, 'option_affine')
test_geo_workflow2.connect(node_reg_aladin2, 'output_affine_transformation', node_jacobian_matrix, 'option_affine')
test_geo_workflow2.connect(node_reg_aladin2, 'output_affine_transformation', node_jacobian_dtm, 'option_affine')

##############
# Draw graph #
##############

#simple
test_geo_workflow2.write_graph()

#detailed
#test_geo_workflow2.write_graph('test_geo_workflow2_graph.dot', graph2use = 'exec')

#######
# Run #
#######

test_geo_workflow2.run()




