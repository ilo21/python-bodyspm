from classdefinitions import Subject, Stimuli
from bodyfunctions import *
import h5py
import numpy as np
import pandas as pd
from scipy import stats
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
import os


# where should the output figures be saved to?
figloc = r"C:\Path to save figures\Embody preprocessed intentionally empty\Figures"
maskloc = r"C:\Path to mask\sample_data"

# path to patient h5 file
datafile = r"C:\Path to patient h5 file\Embody preprocessed intentionally empty\dataset_patients.h5"
# path to control h5 file
datafile_controls = r"C:\Path to control h5 file\Embody preprocessed intentionally empty\dataset_controls.h5"

# read in the relevant masks
back_path = os.path.join(maskloc,'mask_back_new.png')
front_path = os.path.join(maskloc,'mask_front_new.png')

mask_fb = read_in_mask(front_path,back_path)

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

# define colormaps for the plots
hot = plt.cm.get_cmap('hot', 256)
new_cols = hot(np.linspace(0, 1, 256))

cold = np.hstack((np.fliplr(new_cols[:,0:3]),new_cols[:,3][:,None]))
newcolors = np.vstack((np.flipud(cold), new_cols))
newcolors = np.delete(newcolors, np.arange(200, 312, 2), 0)

# make separate plot for each stimulus
for i, cond in enumerate(stim_names.keys()):
    # patient data
    with h5py.File(datafile, 'r') as h:
        patient = h[cond][()]
    # control data
    with h5py.File(datafile_controls, 'r') as c:
        control = c[cond][()]

    # for twosided maps (front and back of body) use colormap 'hot' and scale data to [0,1]
    if stim_names[cond][1] == 1:
        mask = mask_fb
        cmap = 'hot'
        vmin = 0
        vmax = 1
        fig = plt.figure(figsize=(25, 10))
    # for emotion maps (activation and deactivation) use a diverging colormap and scale data to [-1, 1]
    else:
        mask = mask_one
        cmap = ListedColormap(newcolors)
        vmin = -1
        vmax = 1
        fig= plt.figure(figsize=(14,10))

    control_t = np.nanmean(binarize(control.copy()), axis=0)
    masked_control= np.ma.masked_where(mask != 1, control_t)

    patient_t = np.nanmean(binarize(patient.copy()), axis=0)
    masked_kipu= np.ma.masked_where(mask != 1, patient_t)

    if stim_names[cond][1]==1:
        twosamp_t, twosamp_p = compare_groups(patient, control, testtype='z')
    else:
        twosamp_t, twosamp_p = stats.ttest_ind(patient, control, axis=0, nan_policy='omit')
        
    twosamp_p_corrected, twosamp_reject = p_adj_maps(twosamp_p, mask=mask, method='fdr_bh')

    
    twosamp_p_corrected[np.isnan(twosamp_p_corrected)] = 1
    twosamp_t_no_fdr = twosamp_t.copy()

    twosamp_t[twosamp_p_corrected > 0.05] = 0
    masked_twosamp = np.ma.masked_where(mask != 1, twosamp_t)

    twosamp_t_no_fdr[twosamp_p > 0.05] = 0
    masked_twosamp_no_fdr = np.ma.masked_where(mask != 1, twosamp_t_no_fdr)

    ax1 = plt.subplot(142)
    img1 = plt.imshow(masked_kipu, cmap=cmap, vmin=vmin, vmax=vmax)
    ax1.title.set_text('Patients')
    fig.colorbar(img1,fraction=0.046, pad=0.04)
    ax1.axis('off')

    ax2 = plt.subplot(141)
    img2 = plt.imshow(masked_control, cmap=cmap, vmin=vmin, vmax=vmax)
    ax2.title.set_text('Matched controls')
    fig.colorbar(img2, fraction=0.046, pad=0.04)
    ax2.axis('off')

    ax3 = plt.subplot(143)
    img3 = plt.imshow(masked_twosamp, cmap='bwr', vmin=-8, vmax=8)
    ax3.title.set_text('Difference')
    fig.colorbar(img3, fraction=0.046, pad=0.04)
    ax3.axis('off')

    ax4 = plt.subplot(144)
    img4 = plt.imshow(masked_twosamp_no_fdr, cmap='bwr', vmin=-8, vmax=8)
    ax4.title.set_text('Difference, no FDR correction')
    fig.colorbar(img4, fraction=0.046, pad=0.04)
    ax4.axis('off')

    fig.suptitle(stim_names[cond][0], size=20, va='top')
    path2save = os.path.join(figloc,cond+'_controls_patients_pixelwise.png')
    plt.savefig(path2save)
    plt.close()
print("Done")