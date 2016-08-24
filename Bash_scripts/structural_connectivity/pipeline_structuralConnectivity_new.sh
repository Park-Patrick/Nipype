#!/bin/bash

#-------
# Prerequisite: need to import data first
# importT1 <dicom/nifti> <subjid>
# importDicomDTI_dcm2nii <dicom folder> <subjid>
#
# INPUT: location of directory containing subjid
#
# NOTE: Reference T1/T2 images should be available for Distortion correction (extra_mri)
#-------
cd $1 #Change directory to location containing subjid
subjlist="$(ls -d *EPI_*)" #Retrieve list of subjects from input (folder containing subjid)

atlas=MNI152_1mm #Atlas should exist in $PIPELINE_ATLAS_DIR

labelgroup=HarvardOxford #Label group should exist as folder in $PIPELINE_ATLAS_DIR/$atlas/labels/t1

for subj in $subjlist
do

#DTI Processing
preprocDTI $subj

#Camino DTI tractography
caminoProcessDTI $subj
caminoTrackingWholeBrainDTI $subj

#T1 and label processing
preprocT1 $subj
reg_intersubj_aladin t1 ${atlas} $subj
reg_bspline_f3d t1 ${atlas} $subj
propLabels_reg_bspline_f3d t1 ${labelgroup} ${atlas} $subj

#Coregister DTI and propagate labels
reg_intrasubj_aladin t1 dti $subj -r
propLabels_compose_inter_bspline_intra_aladin t1 t1 dti ${labelgroup} ${atlas} $subj -r

#Generate DTI connectivity
subj_dir=$1/$subj # Path to patient specific folder
if [ -e $subj_dir/dti/distortCorrect ]
then
 caminoGenConnectivity $subj -L labels/dti/${labelgroup}_bspline_f3d_rigid_aladin_${atlas}/${labelgroup}-combined-maxprob-thr25-1mm.nii.gz -b dti/distortCorrect/caminoTractographyDTI/wholebrain.Bfloat
else
  
  if [ -e $subj_dir/dti/eddyCorrect ]
  then
   caminoGenConnectivity $subj -L labels/dti/${labelgroup}_bspline_f3d_rigid_aladin_${atlas}/${labelgroup}-combined-maxprob-thr25-1mm.nii.gz -b dti/eddyCorrect/caminoTractographyDTI/wholebrain.Bfloat
  else

   echo "Eddy corrected and/or Distortion corrected DTI data does not exist for $subj"
   continue
  fi
fi  

done

#Generate QC
genOverlay_brainmask $subjlist
genOverlay_affine_atlasReg ${atlas} $subjlist
genOverlay_intrasubj t1 dti $subjlist
genOverlay_bspline_atlasReg ${atlas} $subjlist
