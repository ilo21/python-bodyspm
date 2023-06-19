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


# condition from stim_names
WHICH_CONDITION = '12'
# where should the output figures be saved to?
figloc = r"C:\Path to save figure\Figures"
maskloc = r"C:\Path to mask\sample_data"

# combined dataset location location for patients
datafile = r"C:\Path to patiens h5 file\dataset_patients.h5"

# read in the mask
front_path = os.path.join(maskloc,'mask_front_new.png')
mask_one = read_in_mask(front_path)

# which stimuli do we want to analyse? dictionary, with system stimulus name as key and 
# display name (title for plot) and whether it is twosided (0 for no, 1 for yes) as values
stim_names = {'0': ['Inget särskilt\n(neutral)', 0], 
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
              '12': ['Impuls att skada\ndig själv', 0],
              }

# define colormaps for the plots
hot = plt.cm.get_cmap('hot', 256)
new_cols = hot(np.linspace(0, 1, 256))

cold = np.hstack((np.fliplr(new_cols[:,0:3]),new_cols[:,3][:,None]))
newcolors = np.vstack((np.flipud(cold), new_cols))
newcolors = np.delete(newcolors, np.arange(200, 312, 2), 0)

# make separate plot for impulse
# patient data
with h5py.File(datafile, 'r') as h:
    patient = h[WHICH_CONDITION][()]
# for emotion maps (activation and deactivation) use a diverging colormap and scale data to [-1, 1]
mask = mask_one
cmap = ListedColormap(newcolors)
vmin = -1
vmax = 1
fig= plt.figure(figsize=(6,10))

patient_t = np.nanmean(binarize(patient.copy()), axis=0)
masked_kipu= np.ma.masked_where(mask != 1, patient_t)

ax1 = fig.add_subplot(111)
img1 = plt.imshow(masked_kipu, cmap=cmap, vmin=vmin, vmax=vmax)
ax1.set_title(stim_names[WHICH_CONDITION][0], fontsize=20)
# fig.colorbar(img1,fraction=0.046, pad=0.04)
fig.colorbar(img1,ax=ax1,pad=0.02, fraction=0.036)
ax1.axis('off')
    
    
# fig.suptitle(stim_names[cond][0], size=20, va='top')
path2save = os.path.join(figloc,'Impulse_all_patients_pixelwise.png')
plt.savefig(path2save)
plt.close()
print("Done")