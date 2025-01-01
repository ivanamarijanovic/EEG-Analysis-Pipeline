import os

import matplotlib.pyplot as plt
import mne
import numpy as np
import pandas as pd
import sklearn
from mne_bids import BIDSPath, read_raw_bids


# Define the path to the epoched data file

save_path = '/data/pt_02697/eeg/pilot/data/lisa/processed_data_cold/'
epoched_save_file_name = '_epo.fif'
sub = '06'
save_epochs_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', epoched_save_file_name)

# Load the epoched data
epochs = mne.read_epochs(save_epochs_path, preload=True)

# Montage

montage_file = '/data/gt_gr_eippert_cloud/Temp_sharing/lisa-marie/cfg/standard-10-5-cap385_added_mastoids (copy 3).elp'
montage = mne.channels.read_custom_montage(montage_file)
epochs.set_montage(montage)

# ICA

# Initialize ICA
ica = mne.preprocessing.ICA(n_components=31, method='infomax', random_state=97, max_iter=800) # for sub-06 it has to be 31

# Fit ICA to the epoched data
ica.fit(epochs)


# Saving ICA
save_ICA_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', 'preprocessing-ica.fif')
ica.save(save_ICA_path, overwrite=True)