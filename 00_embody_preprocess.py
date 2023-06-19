
from classdefinitions import Stimuli
from bodyfunctions import preprocess_subjects, make_qc_figures, combine_data
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



# all are true in our case
onesided = [True, True, True, True, True, True, True, True, True, True, True, True, True]
# onesided = [False, False, False, False, False, False, False, False, False, False, False, False, False]
# boolean or list of booleans describing if data is onesided (e.g. emotion body maps, with one image
# representing intensifying and one image representing lessening activation. In this case, one side is deducted from
# the other. Alternative (False) describes situation where both sides of colouring are retained, e.g. touch allowances
# for front and back of body.
# names of emotions
data_emotions = ['Inget särskilt (neutral)', 'Rädsla', 'Ilska', 'Avsky/äckel', 'Ledsenhet/Sorg','Glädje','Förvåning', 'Kärlek','Skam','Avundsjuka','Skuld','Intresse','Impuls att skada dig själv']
# names of files
data_names = ['0', '1', '2', '3', '4','5','6', '7','8','9','10','11','12']
# inputs (path to data)
dataloc = r"C:\Path to collected data\Embody task data"
# output path
outdataloc = r"C:\Path to save processed data\Embody preprocessed intentionally empty"
# path for QC figures
qc_outdataloc =  r"C:\Path to save quality control figures\Embody task QC intentionally empty"
# path to a csv file with subject ids that is necessary for count_pixels script
csv_with_ids = r"C:\Path to save bg file\Embody preprocessed intentionally empty\subject_background.csv"
# list of subjects (folder names)
subnums_control = ['2222', 
                    '3333'
                    ]
subnums_patients = ['5555',
                    '9999'      
                    ]
# all subjects together
subnums = ['2222', 
            '3333', 
            '5555',
            '9999'             
            ]


# define stimulus set
stim = Stimuli(data_names, onesided=onesided,show_names=data_emotions)

# read subjects from web output and write out to a more sensible format
preprocess_subjects(subnums, dataloc, outdataloc, stim, intentionally_empty = True)
########################################################################
# Quality Control All
make_qc_figures(subnums, dataloc, stim, qc_outdataloc)
#######################################################################
# !! run this part separately for the control and patients to create h5 file separately
# then, rename the output h5 and csv files to control/patient
full_dataset = combine_data(outdataloc, subnums_patients, save=True, noImages=False)
bg = full_dataset['bg']
bg.to_csv(csv_with_ids)
print("Done")
