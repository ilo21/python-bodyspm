import os
import sys
import pandas as pd
from classdefinitions import Subject, Stimuli
from bodyfunctions import combine_data, preprocess_subjects, make_qc_figures
import matplotlib.pyplot as plt
import numpy as np

csvname = r"C:\Path to save bg file\python_code_testing\subject_background.csv"
# set up stimuli description
onesided = [True, True, True, True, True, True, True, False, False, False]
# boolean or list of booleans describing if data is onesided (e.g. emotion body maps, with one image
# representing intensifying and one image representing lessening activation. In this case, one side is deducted from
# the other. Alternative (False) describes situation where both sides of colouring are retained, e.g. touch allowances
# for front and back of body.
data_names = ['emotions_0', 'emotions_1', 'emotions_2', 'emotions_3', 'emotions_4','emotions_5','emotions_6', 'sensitivity_0','sensitivity_1','sensitivity_2']
stim_names = ['stim1','stim2','stim3','stim4','stim5', 'pain1', 'pain2'] # potentially add stimulus names for more intuitive data handling

# inputs (path to data)
dataloc = r"C:\Path to collected data\sample_data"
# output path
outdataloc = r"C:\Path to save processed data\python_code_testing"
subnums = ['test_sub_1', 'test_sub_2', 'test_sub_3','test_sub_4']
# bg_files = ['data.txt']
# fieldnames = [['sex','age','height','weight','handedness','education','physical_work','sitting_work','profession','history_of_x','history_of_y','history_of_z']]

# define stimulus set
stim = Stimuli(data_names, onesided=onesided)

######################################################################
# preprocess
# read subjects from web output and write out to a more sensible format
# # preprocess_subjects(subnums, dataloc, outdataloc, stim, bg_files, fieldnames)
# preprocess_subjects(subnums, dataloc, outdataloc, stim)
#######################################################################

# Gather subjects into one dict
subnums = ['test_sub_1', 'test_sub_2', 'test_sub_3','test_sub_4']
grouping = ['foo', 'bar', 'foo', 'bar']

# instead create separate h5 files for each group
subnumsK = ['test_sub_1','test_sub_3']
subnums = ['test_sub_2','test_sub_4']
# run separately for the control and patients to create h5 file separately
full_dataset = combine_data(outdataloc, subnums, save=True, noImages=True)
# full_dataset = combine_data(outdataloc, subnums, groups = grouping, save=True, noImages=False)
# print(full_dataset['groups'])

###################################################################################
# # Quality control
# qc_outdataloc =  r"C:\Users\ilosz01\OneDrive - Linköpings universitet\biofeedback_scripts\EmBody\python-bodyspm-masterJuulia\python_code_testing\QC"
# stim = Stimuli(names=data_names, onesided=onesided)
# make_qc_figures(subnums, dataloc, stim, qc_outdataloc)
###################################################################################

# # Combines a data set from subjects who have been written to file.
# # dataloc: where the subject data files have been saved. Assumes .json files for subjects and stimuli are located in this folder
# # full_dataset = combine_data(outdataloc, subnums, groups = grouping, save=True, noImages=True)
# full_dataset = combine_data(outdataloc, subnums, save=True, noImages=False)

# no background data but run separately for controls and patients to create a map of subject id and file name
# maybe fix later to make ids unique for all subjects (between 1 and 55)
bg = full_dataset['bg']
bg.to_csv(csvname)

# print(full_dataset)
# # indices = lambda searchList, elem: [[i for i, x in enumerate(searchList) if x == e] for e in elem]
# # indices(full_dataset['groups'], ['foo','bar'])

