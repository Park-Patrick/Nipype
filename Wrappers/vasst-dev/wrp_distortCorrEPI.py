from nipype.interfaces.base import(
    TraitedSpec,
    CommandLineInputSpec,
    CommandLine,
    File,
    traits
)
root_dir = '/home/ROBARTS/ppark/Documents/structural_connectivity/terminal_test/'

avgb0 = 'avg_b0.nii.gz'
eddy_dwi = 'eddy_dwi.nii.gz'
mask = 'orig_brainmask.nii.gz'
t1map_ref = 't1map.brain.nii.gz'

distort_work_dir = '/home/ROBARTS/ppark/Documents/structural_connectivity/terminal_test'
distort_dwi = 'distort_dwi.nii.gz'
distort_mask = 'distort_brainmask.nii.gz'

class distortCorrEPIInputSpec(CommandLineInputSpec):
    
    input3DVol = File(exists=True, argstr='%s', mandatory = True,
                      position = 0, desc = 'input3DVol')
                      
    input4DVol = File(exists=True, argstr='%s', mandatory = True,
                      position=1, desc = 'input4DVol')
                      
    inputBrainMask = File(exists=True, argstr='%s', mandatory = True,
                          position=2, desc = 'inputBrainMask')
    
    referenceSkullStripped3D = File(exists=True, argstr='%s', mandatory = True,
                                  position=3, desc = 'referenceSkullStripped3D')
    
    workFolder = File(argstr = '%s', mandatory = True,
                            position = 4, desc = 'workFolder')
                            
    corrected4DVol = File(argstr = '%s', mandatory = True,
                                position = 5, desc = 'corrected4DVol')
                                
    correctedBrainMask = File(argstr = '%s', mandatory = True,
                                    position = 6, desc = 'correctedBrainMask')
                                    

class distortCorrEPIOutputSpec(TraitedSpec):
    output_corrected4DVol = File(exists=True, desc = 'output_corrected4DVol')
    
    output_correctedBrainMask = File(exists=True, desc = 'output_correctedBrainMask')
    

class distortCorrEPI(CommandLine):
    _cmd = 'distortCorrEPI'
    input_spec = distortCorrEPIInputSpec
    output_spec = distortCorrEPIOutputSpec
    
    def _list_outputs(self):
        outputs = self.output_spec().get()
        
        output_corrected4DVol = self.inputs.corrected4DVol
        outputs['output_corrected4DVol'] = output_corrected4DVol
        
        output_correctedBrainMask = self.inputs.correctedBrainMask
        outputs['output_correctedBrainMask'] = output_correctedBrainMask
        

if __name__ == '__main__':
    selfTester = distortCorrEPI()
    selfTester.inputs.input3DVol = root_dir + avgb0
    selfTester.inputs.input4DVol = root_dir + eddy_dwi
    selfTester.inputs.inputBrainMask = root_dir + mask
    selfTester.inputs.referenceSkullStripped3D = root_dir + t1map_ref
    selfTester.inputs.workFolder = distort_work_dir
    selfTester.inputs.corrected4DVol = root_dir + distort_dwi
    selfTester.inputs.correctedBrainMask = root_dir + distort_mask
    print selfTester.cmdline
#    selfTester.run()
    
    
    
