#!/bin/bash
# script: pipeline_7T_to_3T
#   created by jclau 20160107
#
# details:
#   Processing pipeline for 7T to 3T geometric distortion analysis
#   rigid body (lsq6) -> affine (lsq12) -> nlin -> jacobian
#
# prerequisites: run rsync_7T_to_scratch
# TODO: old version of niftyreg?

# /cluster/data/test_geo_dbm/
root_dir=~/EpilepsyDatabase/Projects/test_geo_dbm/

for subj in $@
do

  subj_dir=$root_dir/$subj/

  #### INPUT DATA #################################################################################

  # 3T dataset in subject space
  despot1=$subj_dir/Preop/Despot/despot1_tr90_fa18.nii.gz
  despot1_mask=$subj_dir/Preop/Processed/BrainMask/BrainMask.nii.gz

  # 7T dataset in subject space
  highres=$subj_dir/7T/MPRAGE_std_N4.nii.gz
  highres_bet=$subj_dir/7T/MPRAGE_std_N4_bet.nii.gz
  highres_mask=$subj_dir/7T/MPRAGE_std_N4_bet_BrainMask.nii.gz

  # TODO: also compute deformations of susc_hires to MPRAGE and look at deformities there...
  susc_hires=$subj_dir/7T/Susc3D_MagEchoAvg.nii.gz

  #### OUTPUT DATA ################################################################################

  # defining output data variables
  output_dir=$subj_dir/7T/Processed/7Tto3T/

  # data preprocessing (non-uniformity correction if necessary

  despot1_nuc=$output_dir/despot1_tr90_fa18_nuc.nii.gz
  despot1_nuc_masked=$output_dir/despot1_tr90_fa18_nuc_masked.nii.gz
  # considered using the Preop/Processed/TissueSegBiasCorrect/ but not good correction
  N4BiasFieldCorrection -i $despot1 -o $despot1_nuc
  echo N4BiasFieldCorrection -i $despot1 -o $despot1_nuc
  fslmaths $despot1_nuc -mul $despot1_mask $despot1_nuc_masked
  echo fslmaths $despot1_nuc -mul $despot1_mask $despot1_nuc_masked

  resampled_despot1=$output_dir/despot1_05mm.nii.gz
  resampled_despot1_mask=$output_dir/despot1_05mm_BrainMask.nii.gz

  resampled_highres=$output_dir/MPRAGE_std_N4_05mm.nii.gz
  resampled_highres_bet=$output_dir/MPRAGE_std_N4_bet_05mm.nii.gz
  resampled_highres_mask=$output_dir/MPRAGE_std_N4_05mm_BrainMask.nii.gz

  rigid_xfm=$output_dir/7T_to_3T_rigid_xfm.txt
  rigid_nii=$output_dir/7T_to_3T_rigid.nii

  affine_xfm=$output_dir/7T_to_3T_affine_xfm.txt
  affine_nii=$output_dir/7T_to_3T_affine.nii

  nlin_cpp=$output_dir/7T_to_3T_nlin_cpp.nii
  nlin_nii=$output_dir/7T_to_3T_nlin.nii

  log_jacobian=$output_dir/7T_to_3T_log_jacobian.nii
  mat_jacobian=$output_dir/7T_to_3T_mat_jacobian.nii
  jacobian=$output_dir/7T_to_3T_jacobian.nii

  #### PROCESSING #################################################################################

  mkdir -p $output_dir

  # create mask from bet extracted dataset by binarizing
  fslmaths $highres_bet -bin $highres_mask

  # resample 7T and 3T datasets as well as their masks prior to registration
  mri_convert $highres -vs 0.5 0.5 0.5 $resampled_highres
  mri_convert $highres_bet -vs 0.5 0.5 0.5 $resampled_highres_bet
  mri_convert $highres_mask -vs 0.5 0.5 0.5 $resampled_highres_mask

  mri_convert $despot1_nuc_masked -vs 0.5 0.5 0.5 $resampled_despot1
  mri_convert $despot1_mask -vs 0.5 0.5 0.5 $resampled_despot1_mask

  # rigid body registration: highres -> standard
  # TODO: consider optimizing parameters (flags)
  # TODO: consider incorporating dilated masks for optimizing
#  reg_aladin -ref $resampled_despot1 -flo $resampled_highres -rigOnly -rmask $resampled_despot1_mask -fmask $resampled_highres_mask -aff $rigid_xfm -res $rigid_nii
  echo reg_aladin -ref $resampled_despot1 -flo $resampled_highres_bet -rigOnly -aff $rigid_xfm -res $rigid_nii
  reg_aladin -ref $resampled_despot1 -flo $resampled_highres_bet -rigOnly -aff $rigid_xfm -res $rigid_nii

  # affine 12-DOF registration: highres -> standard
#  reg_aladin -ref $resampled_despot1 -flo $resampled_highres -rmask $resampled_despot1_mask -fmask $resampled_highres_mask -inaff $rigid_xfm -aff $affine_xfm -res $affine_nii
  echo reg_aladin -ref $resampled_despot1 -flo $resampled_highres_bet -inaff $rigid_xfm -aff $affine_xfm -res $affine_nii
  reg_aladin -ref $resampled_despot1 -flo $resampled_highres_bet -inaff $rigid_xfm -aff $affine_xfm -res $affine_nii
  
  # nonlinear registration: highres -> standard
#  reg_f3d -ref $resampled_despot1 -flo $resampled_highres -rmask $resampled_despot1_mask -fmask $resampled_highres_mask -aff $affine_xfm -cpp $nlin_cpp -res $nlin_nii
  echo reg_f3d -ref $resampled_despot1 -flo $resampled_highres_bet -aff $affine_xfm -cpp $nlin_cpp -res $nlin_nii
  reg_f3d -ref $resampled_despot1 -flo $resampled_highres_bet -aff $affine_xfm -cpp $nlin_cpp -res $nlin_nii

  # computation of Jacobian determinant files
  # TODO: modulating with affine transform but does this actually do anything??
  reg_jacobian -ref $resampled_despot1 -cpp $nlin_cpp -aff $affine_xfm -jacL $log_jacobian
  reg_jacobian -ref $resampled_despot1 -cpp $nlin_cpp -aff $affine_xfm -jacM $mat_jacobian
  reg_jacobian -ref $resampled_despot1 -cpp $nlin_cpp -aff $affine_xfm -jac $jacobian

done
