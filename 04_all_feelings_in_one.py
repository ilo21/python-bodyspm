from bodyfunctions import *
import h5py
import numpy as np
import scipy.misc
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib import gridspec
from PIL import Image
from operator import add
from mpl_toolkits.axes_grid1 import make_axes_locatable

# excluded condition = impulse (will not be shown to compare with controls)
EXCLUDE = "12"

outfilename = r"C:\Path to save figure\Embody preprocessed intentionally empty\Figures\_comparison_preview.png"
suptitle = 'Average emotions'

# patients
datafile1 =  r"C:\Path to patients h5 file\Embody preprocessed intentionally empty\dataset_patients.h5"
# controls
datafile = r"C:\Path to controls h5 file\Embody preprocessed intentionally empty\dataset_controls.h5"

maskloc =  r"C:\Path to mask\sample_data"

stim_names = {'0': ['Inget särskilt(neutral)', 0], 
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
# show all emotions except one
total_emotions = len(stim_names)-1

# read in the relevant masks
back_path = os.path.join(maskloc,'mask_back_new.png')
front_path = os.path.join(maskloc,'mask_front_new.png')
# mask_fb = read_in_mask(maskloc + 'mask_front_new.png', maskloc + 'mask_back_new.png')
mask_fb = read_in_mask(front_path,back_path)
# mask_one = read_in_mask(maskloc + 'mask_front_new.png')
mask_one = read_in_mask(front_path)

hot = plt.cm.get_cmap('hot', 256)
new_cols = hot(np.linspace(0, 1, 256))

cold = np.hstack((np.fliplr(new_cols[:,0:3]),new_cols[:,3][:,None]))
newcolors = np.vstack((np.flipud(cold), new_cols))
newcolors = np.delete(newcolors, np.arange(200, 312, 2), 0)
cmap = ListedColormap(newcolors)
#cmap = 'coolwarm'
vmin = -1
vmax = 1

fig, axs = plt.subplots(2,total_emotions, figsize=(25, 13), facecolor='w', edgecolor='k')
axs = axs.ravel()
all_figs = np.zeros([mask_one.shape[0], mask_one.shape[1]])

for i, cond in enumerate(stim_names.keys()):
    for j, file in enumerate([datafile1, datafile]):
        if cond != EXCLUDE:
            print('reading in ' + cond)
            with h5py.File(file, 'r') as h:
                data = h[cond][()]
                all_n = np.count_nonzero(~np.isnan(data[:,1,1]))
                all_figs = np.nanmean(binarize(data.copy()), axis=0)
                masked_data = np.ma.masked_where(mask_one != 1,all_figs)
            if j == 0:
                imind = i
            else:
                imind = i+total_emotions
            im = axs[imind].imshow(masked_data, cmap=cmap, vmin=vmin, vmax=vmax)
            axs[imind].set_xticklabels([])
            axs[imind].set_yticklabels([])
            axs[imind].set_axis_off()
            if j==0:
                axs[imind].set_title(stim_names[cond][0],fontsize=12)

fig.subplots_adjust(wspace=0, hspace=0)
[[x00,y00],[x01,y01]] = axs[6].get_position().get_points()
[[x10,y10],[x11,y11]] = axs[23].get_position().get_points()
pad = 0.022; width = 0.01
cbar_ax = fig.add_axes([x11+pad, y10+pad, width, y01-y10-2*pad])
axcb = fig.colorbar(im, cax=cbar_ax)
# axcb.set_label(label='Proportion of subjects', fontsize=12, labelpad=-120)
axcb.ax.tick_params(labelsize=20)


plt.gcf().text(0.11, 0.65, "Patients", fontsize=24, rotation=90)
plt.gcf().text(0.11, 0.25, "Controls", fontsize=24, rotation=90)
plt.gcf().text(0.90, 0.885, "Activation", fontsize=20)
plt.gcf().text(0.90, 0.098, "Inactivation", fontsize=20)

plt.savefig(outfilename)
plt.close()
# plt.show()
print("Done")
