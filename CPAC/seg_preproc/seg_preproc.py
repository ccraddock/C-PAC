import os
import sys
import commands
import nipype.pipeline.engine as pe
import nipype.algorithms.rapidart as ra
import nipype.interfaces.afni as afni
import nipype.interfaces.fsl as fsl
import nipype.interfaces.io as nio
import nipype.interfaces.utility as util
from CPAC.seg_preproc import *

def create_seg_preproc():


    """
    Segment the Subject's Anatomical brain into cerebral spinal fluids, white matter and gray matter.
    Threshold and binarize them.

    Parameters
    ----------

    None : None

    Returns
    -------

    seg_preproc : workflow

        Workflow Object for Segmentation Workflow


    

    Examples
    --------

    >>> seg = create_seg_preproc()
    >>> seg.inputs.inputspec.preprocessed_mask = os.path.abspath('/home/data/Projects/Pipelines_testing/Dickstein/subjects/s1001/func/original/rest_pp_mask.nii.gz')
    >>> seg.inputs.inputspec.standard_res_brain = standard_res_brain
    >>> seg.inputs.inputspec.example_func = os.path.abspath('/home/data/Projects/Pipelines_testing/Dickstein/subjects/s1001/func/original/example_func.nii.gz')
    >>> seg.inputs.inputspec.highres2example_func_mat = os.path.abspath('/home/data/Projects/Pipelines_testing/Dickstein/subjects/s1001/func/original/reg/highres2example_func.mat')
    >>> seg.inputs.inputspec.stand2highres_warp = os.path.abspath('/home/data/Projects/Pipelines_testing/Dickstein/subjects/s1001/anat/reg/stand2highres_warp.nii.gz')
    >>> seg.inputs.inputspec.PRIOR_CSF = os.path.abspath('/home/data/Projects/C-PAC/tissuepriors/2mm/avg152T1_csf_bin.nii.gz')
    >>> seg.inputs.inputspec.PRIOR_WHITE = os.path.abspath('/home/data/Projects/C-PAC/tissuepriors/2mm/avg152T1_white_bin.nii.gz')
    >>> seg.inputs.inputspec.PRIOR_GRAY = os.path.abspath('/home/data/Projects/C-PAC/tissuepriors/2mm/avg152T1_gray_bin.nii.gz')
    >>> seg.inputs.inputspec.brain = os.path.abspath('/home/data/Projects/Pipelines_testing/Dickstein/subjects/s1001/anat/mprage_brain.nii.gz')
    >>> seg.inputs.inputspec.standard_res_brain = os.path.abspath('/usr/share/fsl/4.1/data/standard/MNI152_T1_2mm_brain.nii.gz')
    >>> seg.inputs.csf_threshold.csf_threshold = [0.4]
    >>> seg.inputs.wm_threshold.wm_threshold = [0.66]
    >>> seg.inputs.gm_threshold.gm_threshold = [0.2]
    >>> seg.get_node('csf_threshold').iterables = ('csf_threshold', [0.4])
    >>> seg.get_node('wm_threshold').iterables = ('wm_threshold', [0.66])
    >>> seg.get_node('gm_threshold').iterables = ('gm_threshold', [0.2]) 
    >>> seg_preproc.run() # doctest: +SKIP


    Notes
    -----

    `Source <https://github.com/openconnectome/C-PAC/blob/master/CPAC/seg_preproc/seg_preproc.py>`_ 

    Workflow Inputs: ::
 
        csf_threshold.csf_threshold : list (float)
            Threshold of Cerebral Spinal Fluid probabilities 
    
    
        wm_threshold.wm_threshold : list (float) 
            Threshold of White Matter probabilities
    
        gm_threshold.gm_threshold : list (float) 
            Threshold of Gray Matter probabilities
    
        inputspec.preprocessed_mask : string (existing nifti file)
            Mask of the preprocessed functional file generated by functional preprocessing workflow.
    
        inputspec.brain : string (existing nifti file)
            Anatomical image(without skull)
    
        inputspec.standard_res_brain : string (existing nifti file)
            FSL Standard Anatomical Brain. User picks the resolution
    
        inputspec.example_func : string (existing nifti file)
            Mean functional image from the func_preproc workflow
    
        inputspec.highres2example_func_mat : string (existing affine transformation .mat file)
            File for transformation from anatomical space to functional space
    
    
        inputspec.standard2highres_warp : string (existing nifti file)
            Anatomical image in native space generated from the anatomical image in Standard space in the registration workflow
    
        inputspec.PRIOR_CSF : string (existing nifti file)
            FSL Standard CSF Tissue prior image , binarized with threshold of 0.4 
    
        inputspec.PRIOR_GRAY : string (existing nifti file)
            FSL Standard GRAY Matter Tissue prior image , binarized with threshold of 0.66
    
        inputspec.PRIOR_WHITE : string (existing nifti file)
            FSL Standard White Matter Tissue prior image , binarized with threshold of 0.2
        
    Workflow Outputs: ::

        outputspec.csf_t12func : string (nifti file)
            outputs CSF probabilities(in T1 space) registered to functional space        
    
        outputspec.csf_mni2func : string (nifti file)
            outputs CSF probabilities(in MNI space) registered to functional space
    
        outputspec.csf_combo : string (nifti file)
            outputs Image containing overlap between csf_t12func and csf_mni2func
    
        outputspec.csf_bin : string (nifti file)
            outputs image after Thresholding and binarizing csf_combo
    
        outputspec.csf_mask : string (nifti file)
            outputs image after masking csf_combo with inputspec.preprocessed_mask
    
        outputspec.gm_t12func : string (nifti file)
            outputs GRAY Matter probabilities(in T1 space) registered to functional space
    
        outputspec.gm_mni2func : string (nifti file)
            outputs Gray Matter probabilities(in MNI space) registered to functional space
    
        outputspec.gm_combo : string (nifti file)
            outputs image containing overlap between gm_t12func and gm_mni2func
    
        outputspec.gm_bin : string (nifti file)
            outputs image after Thresholding and binarizing gm_combo
    
        outputspec.gm_mask : string (nifti file)
            outputs image after masking gm_combo with inputspec.preprocessed_mask
    
        outputspec.wm_t12func : string (nifti file)
            outputs White Matter probabilities(in T1 space) registered to functional space
    
        outputspec.wm_mni2func : string (nifti file)
            outputs White Matter probabilities(in MNI space) registered to functional space
        
        outputspec.wm_combo : string (nifti file)
            outputs image containing overlap between wm_t12func and wm_mni2func
    
        outputspec.wm_bin : string (nifti file)
            outputs image after Thresholding and binarizing wm_combo
    
        outputspec.wm_mask : string (nifti file)
            outputs image after masking wm_combo with inputspec.preprocessed_mask
    
        outputspec.probability_maps : string (nifti file)
            outputs individual probability maps (output from brain segmentation using FAST)
    
        outputspec.mixeltype : string (nifti file)
            outputs mixeltype volume file _mixeltype (output from brain segmentation using FAST)
    
        outputspec.partial_volume_map : string (nifti file)
            outputs partial volume file _pveseg (output from brain segmentation using FAST)
    
        outputspec.partial_volume_files : string (nifti file)
            outputs partial volume estimate files _pve_ (output from brain segmentation using FAST)


    Order of commands:

    - Segment the Anatomical brain. For details see `fast <http://www.fmrib.ox.ac.uk/fsl/fast4/index.html>`_::

        fast
        -t 1
        -g
        -p
        -o segment
        mprage_brain.nii.gz
    
    - Register CSF template in T1 space to native space. For details see `flirt <http://www.fmrib.ox.ac.uk/fsl/flirt/index.html>`_::
    
        flirt
        -in segment_prob_0
        -ref example_func.nii.gz
        -applyxfm
        -init highres2example_func.mat
        -out csf_t12func
 
    - Register CSF template in MNI space to native space. For details see `applywarp <http://www.fmrib.ox.ac.uk/fsl/fnirt/warp_utils.html#applywarp>`_::
    
        applywarp
        --ref=example_func.nii.gz
        --in=PRIOR_CSF
        --warp=stand2highres_warp.nii.gz
        --postmat=highres2example_func.mat
        --out=csf_mni2func
        --interp=nn

    - Find overlap between csf_t12func and csf_mni2func. For details see  `fslmaths <http://www.fmrib.ox.ac.uk/fslcourse/lectures/practicals/intro/index.htm>`_::

        fslmaths
        csf_t12func.nii.gz
        -mas csf_mni2func.nii.gz
        csf_combo.nii.gz

    - Threshold and binarize CSF probability map ::

        fslmaths
        csf_combo.nii.gz
        -thr 0.4
        -bin csf_bin.nii.gz

    - Generate CSF csf_mask, by applying preprocessed_mask(also called global_mask) to csf_bin ::

        fslmaths
        csf_bin.nii.gz
        -mas global_mask.nii.gz
        csf_mask

    - Register WM template in T1 space to native space ::
    
        flirt
        -in segment_prob_2
        -ref example_func.nii.gz
        -applyxfm
        -init highres2example_func.mat
        -out wm_t12func
 
    - Register WM template in MNI space to native space ::
    
        applywarp
        --ref=example_func.nii.gz
        --in=PRIOR_WM
        --warp=stand2highres_warp.nii.gz
        --postmat=highres2example_func.mat
        --out=wm_mni2func
        --interp=nn

    - Find overlap between wm_t12func and wm_mni2func ::

        fslmaths
        wm_t12func.nii.gz
        -mas wm_mni2func.nii.gz
        wm_combo.nii.gz

    - Threshold and binarize WM probability map ::

        fslmaths
        wm_combo.nii.gz
        -thr 0.4
        -bin wm_bin.nii.gz

    - Generate WM csf_mask, by applying preprocessed_mask(also called global_mask) to wm_bin ::

        fslmaths
        wm_bin.nii.gz
        -mas global_mask.nii.gz
        wm_mask

    - Register GM template in T1 space to native space ::
    
        flirt
        -in segment_prob_1
        -ref example_func.nii.gz
        -applyxfm
        -init highres2example_func.mat
        -out gm_t12func
 
    - Register GM template in MNI space to native space ::
    
        applywarp
        --ref=example_func.nii.gz
        --in=PRIOR_GM
        --warp=stand2highres_warp.nii.gz
        --postmat=highres2example_func.mat
        --out=gm_mni2func
        --interp=nn

    - Find overlap between gm_t12func and gm_mni2func ::

        fslmaths
        gm_t12func.nii.gz
        -mas gm_mni2func.nii.gz
        gm_combo.nii.gz

    - Threshold and binarize GM probability map ::

        fslmaths
        gm_combo.nii.gz
        -thr 0.4
        -bin gm_bin.nii.gz

    - Generate GM csf_mask, by applying preprocessed_mask(also called global_mask) to gm_bin ::

        fslmaths
        gm_bin.nii.gz
        -mas global_mask.nii.gz
        gm_mask

    Execution Graph:
    
    .. image:: ../images/seg_preproc_graph.dot.png
        :width: 1100
        :height: 480
    """

    preproc = pe.Workflow(name='seg_preproc')
    inputNode = pe.Node(util.IdentityInterface(fields=['preprocessed_mask',
                                                'brain',
                                                'standard_res_brain',
                                                'example_func',
                                                'highres2example_func_mat',
                                                'stand2highres_warp',
                                                'PRIOR_CSF',
                                                'PRIOR_GRAY',
                                                'PRIOR_WHITE']),
                        name='inputspec')

    inputnode_csf_threshold = pe.Node(util.IdentityInterface(
                                    fields=['csf_threshold']),
                             name='csf_threshold')

    inputnode_wm_threshold = pe.Node(util.IdentityInterface(
                                    fields=['wm_threshold']),
                             name='wm_threshold')

    inputnode_gm_threshold = pe.Node(util.IdentityInterface(
                                    fields=['gm_threshold']),
                             name='gm_threshold')

    outputNode = pe.Node(util.IdentityInterface(fields=['csf_t12func',
                                                    'csf_mni2func',
                                                    'csf_combo',
                                                    'csf_bin',
                                                    'csf_mask',
                                                    'gm_t12func',
                                                    'gm_mni2func',
                                                    'gm_combo',
                                                    'gm_bin',
                                                    'gm_mask',
                                                    'global_mask',
                                                    'wm_t12func',
                                                    'wm_mni2func',
                                                    'wm_combo',
                                                    'wm_bin',
                                                    'probability_maps',
                                                    'mixeltype',
                                                    'partial_volume_map',
                                                    'partial_volume_files',
                                                    'wm_mask']),
                        name='outputspec')

    def form_threshold_string(threshold):

        return '-thr %f -bin ' % (threshold)

    segment = pe.Node(interface=fsl.FAST(),
                          name='segment')
    segment.inputs.img_type = 1
    segment.inputs.segments = True
    segment.inputs.probability_maps = True
    segment.inputs.out_basename = 'segment'

    csf_t1_to_native = pe.MapNode(interface=fsl.FLIRT(),
                           name='csf_t1_to_native',
                           iterfield=['reference',
                           'in_matrix_file'])
    csf_t1_to_native.inputs.apply_xfm = True

    csf_mni_to_native = pe.MapNode(interface=fsl.ApplyWarp(),
                          name='csf_mni_to_native',
                          iterfield=['ref_file',
                          'postmat'])
    csf_mni_to_native.inputs.interp = 'nn'

    wm_mni_to_native = csf_mni_to_native.clone('wm_mni_to_native')

    overlap_csf_with_prior = pe.MapNode(interface=fsl.MultiImageMaths(),
                             name='overlap_csf_with_prior',
                             iterfield=['in_file',
                             'operand_files'])
    str1 = '-mas %s '
    overlap_csf_with_prior.inputs.op_string = str1

    binarize_threshold_csf = pe.MapNode(interface=fsl.ImageMaths(),
                            name='binarize_threshold_csf',
                            iterfield=['in_file'])

    csf_mask = pe.MapNode(interface=fsl.MultiImageMaths(),
                          name='csf_mask',
                          iterfield=['in_file',
                          'operand_files'])
    str1 = '-mas %s '
    csf_mask.inputs.op_string = str1

    overlap_wm_with_prior = pe.MapNode(interface=fsl.MultiImageMaths(),
                            name='overlap_wm_with_prior',
                            iterfield=['in_file',
                            'operand_files'])
    str1 = '-mas %s '
    overlap_wm_with_prior.inputs.op_string = str1

    binarize_threshold_wm = pe.MapNode(interface=fsl.ImageMaths(),
                             name='binarize_threshold_wm',
                             iterfield=['in_file'])

    wm_t1_to_native = pe.MapNode(interface=fsl.FLIRT(),
                            name='wm_t1_to_native',
                            iterfield=['reference',
                            'in_matrix_file'])
    wm_t1_to_native.inputs.apply_xfm = True

    wm_mask = csf_mask.clone('wm_mask')

    gm_t1_to_native = wm_t1_to_native.clone('gm_t1_to_native')
    binarize_threshold_gm = binarize_threshold_csf.clone('binarize_threshold_gm')
    gm_mni_to_native = wm_mni_to_native.clone('gm_mni_to_native')
    overlap_gm_with_prior = overlap_wm_with_prior.clone('overlap_gm_with_prior')
    gm_mask = csf_mask.clone('gm_mask')

    preproc.connect(inputNode, 'brain',
                    segment, 'in_files')
    preproc.connect(segment, ('probability_maps', pick_wm_0),
                    csf_t1_to_native, 'in_file')
    preproc.connect(inputNode, 'example_func',
                    csf_t1_to_native, 'reference')
    preproc.connect(inputNode, 'highres2example_func_mat',
                    csf_t1_to_native, 'in_matrix_file')
    preproc.connect(inputNode, 'example_func',
                    csf_mni_to_native, 'ref_file')
    preproc.connect(inputNode, 'stand2highres_warp',
                    csf_mni_to_native, 'field_file')
    preproc.connect(inputNode, 'PRIOR_CSF',
                    csf_mni_to_native, 'in_file')
    preproc.connect(inputNode, 'highres2example_func_mat',
                    csf_mni_to_native, 'postmat')
    preproc.connect(csf_t1_to_native, 'out_file',
                    overlap_csf_with_prior, 'in_file')
    preproc.connect(csf_mni_to_native, 'out_file',
                    overlap_csf_with_prior, 'operand_files')
    preproc.connect(overlap_csf_with_prior, 'out_file',
                    binarize_threshold_csf, 'in_file')
    preproc.connect(inputnode_csf_threshold,
                    ('csf_threshold', form_threshold_string),
                    binarize_threshold_csf, 'op_string')
    preproc.connect(binarize_threshold_csf, 'out_file',
                    csf_mask, 'in_file')
    preproc.connect(inputNode, 'preprocessed_mask',
                    csf_mask, 'operand_files')
    preproc.connect(segment,
                    ('probability_maps', pick_wm_2),
                    wm_t1_to_native, 'in_file')
    preproc.connect(inputNode, 'example_func',
                    wm_t1_to_native, 'reference')
    preproc.connect(inputNode, 'highres2example_func_mat',
                    wm_t1_to_native, 'in_matrix_file')
    preproc.connect(inputNode, 'example_func',
                    wm_mni_to_native, 'ref_file')
    preproc.connect(inputNode, 'stand2highres_warp',
                    wm_mni_to_native, 'field_file')
    preproc.connect(inputNode, 'PRIOR_WHITE',
                    wm_mni_to_native, 'in_file')
    preproc.connect(inputNode, 'highres2example_func_mat',
                    wm_mni_to_native, 'postmat')
    preproc.connect(wm_t1_to_native, 'out_file',
                    overlap_wm_with_prior, 'in_file')
    preproc.connect(wm_mni_to_native, 'out_file',
                    overlap_wm_with_prior, 'operand_files')
    preproc.connect(overlap_wm_with_prior, 'out_file',
                    binarize_threshold_wm, 'in_file')
    preproc.connect(inputnode_wm_threshold,
                    ('wm_threshold', form_threshold_string),
                    binarize_threshold_wm, 'op_string')
    preproc.connect(binarize_threshold_wm, 'out_file',
                    wm_mask, 'in_file')
    preproc.connect(inputNode, 'preprocessed_mask',
                    wm_mask, 'operand_files')

    ##gray matter mask
    preproc.connect(segment,
                    ('probability_maps', pick_wm_1),
                    gm_t1_to_native, 'in_file')
    preproc.connect(inputNode, 'example_func',
                    gm_t1_to_native, 'reference')
    preproc.connect(inputNode, 'highres2example_func_mat',
                    gm_t1_to_native, 'in_matrix_file')
    preproc.connect(inputNode, 'example_func',
                    gm_mni_to_native, 'ref_file')
    preproc.connect(inputNode, 'stand2highres_warp',
                    gm_mni_to_native, 'field_file')
    preproc.connect(inputNode, 'PRIOR_GRAY',
                    gm_mni_to_native, 'in_file')
    preproc.connect(inputNode, 'highres2example_func_mat',
                    gm_mni_to_native, 'postmat')
    preproc.connect(gm_t1_to_native, 'out_file',
                    overlap_gm_with_prior, 'in_file')
    preproc.connect(gm_mni_to_native, 'out_file',
                    overlap_gm_with_prior, 'operand_files')
    preproc.connect(overlap_gm_with_prior, 'out_file',
                    binarize_threshold_gm, 'in_file')
    preproc.connect(inputnode_gm_threshold,
                    ('gm_threshold', form_threshold_string),
                    binarize_threshold_gm, 'op_string')
    preproc.connect(binarize_threshold_gm, 'out_file',
                    gm_mask, 'in_file')
    preproc.connect(inputNode, 'preprocessed_mask',
                    gm_mask, 'operand_files')

    preproc.connect(segment, 'probability_maps',
                    outputNode, 'probability_maps')
    preproc.connect(segment, 'mixeltype',
                    outputNode, 'mixeltype')
    preproc.connect(segment, 'partial_volume_files',
                    outputNode, 'partial_volume_files')
    preproc.connect(segment, 'partial_volume_map',
                    outputNode, 'partial_volume_map')
    preproc.connect(csf_t1_to_native, 'out_file',
                    outputNode, 'csf_t12func')
    preproc.connect(csf_mni_to_native, 'out_file',
                    outputNode, 'csf_mni2func')
    preproc.connect(overlap_csf_with_prior, 'out_file',
                    outputNode, 'csf_combo')
    preproc.connect(binarize_threshold_csf, 'out_file',
                    outputNode, 'csf_bin')
    preproc.connect(csf_mask, 'out_file',
                    outputNode, 'csf_mask')
    preproc.connect(inputNode, 'preprocessed_mask',
                    outputNode, 'global_mask')
    preproc.connect(wm_t1_to_native, 'out_file',
                    outputNode, 'wm_t12func')
    preproc.connect(wm_mni_to_native, 'out_file',
                    outputNode, 'wm_mni2func')
    preproc.connect(overlap_wm_with_prior, 'out_file',
                    outputNode, 'wm_combo')
    preproc.connect(binarize_threshold_wm, 'out_file',
                    outputNode, 'wm_bin')
    preproc.connect(wm_mask, 'out_file',
                    outputNode, 'wm_mask')
    preproc.connect(gm_t1_to_native, 'out_file',
                    outputNode, 'gm_t12func')
    preproc.connect(gm_mni_to_native, 'out_file',
                    outputNode, 'gm_mni2func')
    preproc.connect(overlap_gm_with_prior, 'out_file',
                    outputNode, 'gm_combo')
    preproc.connect(binarize_threshold_gm, 'out_file',
                    outputNode, 'gm_bin')
    preproc.connect(gm_mask, 'out_file',
                    outputNode, 'gm_mask')

    return preproc


