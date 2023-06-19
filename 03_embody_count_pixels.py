import os
import sys
import pandas as pd
from bodyfunctions import *
import numpy as np
import csv



bgdatapath1 =   r"C:\Path to controls bg csv file\Embody preprocessed intentionally empty\controls_background.csv"
bgdatapath2 =   r"C:\Path to patiens bg csv file\Embody preprocessed intentionally empty\patients_background.csv"
dataloc = r"C:\Path to processed data\Embody preprocessed intentionally empty"
outfilename1 = r"C:\Path to save controls results\Embody preprocessed intentionally empty\controls_background_with_activations.csv"
outfilename2 =r"C:\Path to save patients results\Embody preprocessed intentionally empty\patients_background_with_activations.csv"

maskloc =  r"C:\Path to mask\sample_data"

# controls 
datafile1 = r"C:\Path to controls h5 file\Embody preprocessed intentionally empty\dataset_controls.h5"
# patients
datafile2 = r"C:\Path to patients h5 file\Embody preprocessed intentionally empty\dataset_patients.h5"
# read in the relevant masks
front_path = os.path.join(maskloc,'mask_front_new.png')
# mask_one = read_in_mask(maskloc + 'mask_front_new.png')
mask_one = read_in_mask(front_path)

# which stimuli do we want to analyse? dictionary, with system stimulus name as key and 
# display name (title for plot) and whether it is twosided (0 for no, 1 for yes) as values
stim_names = {'0': ['Inget särskilt (neutral)', 0], 
              '1': ['Rädsla', 0], 
              '2': ['Ilska', 0],
              '3': ['Avsky/äckel', 0], 
              '4': ['Ledsenhet/Sorg', 0], 
              '5': ['Glädje', 0],
              '6': ['Förvåning', 0],
              '7': ['Kärlek', 0],
              '8': ['Skam', 0], 
              '9': ['Avundsjuka', 0],
              '10': ['Skuld', 0],
              '11': ['Intresse', 0],
              '12': ['Impuls att skada dig själv', 0],
              }
################################################################
# for controls
bg = pd.read_csv(bgdatapath1)


for j, cond in enumerate(stim_names.keys()):
    with h5py.File(datafile1, 'r') as h:
        data = h[cond][()]
    mask_use = mask_one
    pos_n, pos_prop, neg_n, neg_prop = count_pixels_posneg(data, mask_use)
    bg[stim_names[cond][0] + '_pos_color'] = pos_prop
    bg[stim_names[cond][0] + '_neg_color'] = neg_prop


bg.to_csv(outfilename1, na_rep='NaN',index=False,encoding="utf-8-sig")
# there should be no negative values
################################################################
# for patients
bg2 = pd.read_csv(bgdatapath2)


for j, cond in enumerate(stim_names.keys()):
    with h5py.File(datafile2, 'r') as h:
        data = h[cond][()]
    mask_use = mask_one
    pos_n, pos_prop, neg_n, neg_prop = count_pixels_posneg(data, mask_use)
    bg2[stim_names[cond][0] + '_pos_color'] = pos_prop
    bg2[stim_names[cond][0] + '_neg_color'] = neg_prop


bg2.to_csv(outfilename2, na_rep='NaN',index=False,encoding="utf-8-sig")
# there should be no negative values
print("Done")