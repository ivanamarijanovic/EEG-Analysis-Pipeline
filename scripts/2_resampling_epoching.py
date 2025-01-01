import os

import matplotlib.pyplot as plt
import mne
import numpy as np
import pandas as pd
from mne_bids import BIDSPath, read_raw_bids

# Define the path to the filtered raw data file
save_path = '/data/pt_02697/eeg/pilot/data/lisa/processed_data_cold/'
sub = '06'
save_file_name = 'filtered_raw.fif'
save_file_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', save_file_name)

# Load the filtered raw data
loaded_raw = mne.io.read_raw_fif(save_file_path, preload=True)

# Epoching

events, event_id = mne.events_from_annotations(loaded_raw)

tmin = -1
tmax = 3

epochs = mne.Epochs(loaded_raw, events, event_id, tmin, tmax, baseline=None, preload=True)

epochs = epochs.resample(sfreq=500)

epochs.plot(n_epochs=1,n_channels=32)
plt.show(block=True)

epochs.drop_bad()


# Saving epochs

save_epochs_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', '_epo.fif')
epochs.save(save_epochs_path, overwrite=True)