import os

import matplotlib.pyplot as plt
import mne
import numpy as np
import pandas as pd
import sklearn
import sys
from mne_bids import BIDSPath, read_raw_bids

from mne.time_frequency import (
    tfr_multitaper,
    tfr_stockwell,
    tfr_morlet,
    tfr_array_morlet,
    AverageTFR)

# Paths
subject_ids = ['01', '02', '03', '04', '05', '06']
conditions = ['0°C', '10°C', '18°C', '22°C']
save_path = '/data/pt_02697/eeg/pilot/data/lisa/processed_data_cold/'

all_epochs = []

for sub in subject_ids:

    plots_ica_save_file_name = 'drop_preprocessing-ica.fif'
    save_ICA_plots_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', 'drop_preprocessing-ica.fif')

    ica_save_file_name = 'preprocessing-ica.fif'
    save_ica_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', ica_save_file_name)

    epoched_save_file_name = 'preprocessed_epochs_epo.fif'
    save_epochs_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', epoched_save_file_name)

    save_file_name = 'filtered_raw.fif'
    save_file_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', save_file_name)

    evoked_save_file_name = 'evoked-ave.fif'
    save_evoked_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', evoked_save_file_name)

    # Interpolation
    raw_data_path = os.path.join(save_path, 'sub-06'.format(sub), 'eeg', save_file_name)
    raw = mne.io.read_raw_fif(raw_data_path, preload=True)
    raw.pick_channels(ch_names=[ch for ch in raw.ch_names if ch != 'T7'])
    raw.interpolate_bads()

    # Loading data
    ica = mne.preprocessing.read_ica(save_ICA_plots_path)
    loaded_raw = mne.io.read_raw_fif(save_file_path)
    evoked = mne.read_evokeds(save_evoked_path)

    epochs = mne.read_epochs(save_epochs_path)
    all_epochs.append(epochs)

    # Montage
    montage_file = '/data/gt_gr_eippert_cloud/Temp_sharing/lisa-marie/cfg/standard-10-5-cap385_added_mastoids (copy 3).elp'
    montage = mne.channels.read_custom_montage(montage_file)
    epochs.set_montage(montage)

    epochs.info['bads'] = ['T7']

combined_epochs = mne.concatenate_epochs(all_epochs)


# TFRs
freqs = np.arange(1, 101)
fmin = 1
fmax = 101


# TFR Stockwell transformation
tfr = tfr_stockwell(combined_epochs, fmin=fmin, fmax=fmax, return_itc=False, verbose=True)
tfr.plot(['Cz', 'C4', 'T8', 'CP6', 'CP2', 'FCz'], baseline=(-0.5, -0.2), mode='percent', title='auto', combine=None,
         tmin=-0.5, tmax=1, vmin=-0.6, vmax=0.6)
plt.show(block=False)


# TFR multitaper transformation
tfr = tfr_multitaper(combined_epochs, freqs=freqs, return_itc=False, verbose=True, time_bandwidth=2.0, n_cycles=freqs/2)
tfr.plot(['Cz', 'C4', 'T8', 'CP6', 'CP2', 'FCz'], baseline=(-0.5, -0.2), mode='percent', title='auto', combine=None,
         tmin=-0.5, tmax=1)
plt.show(block=False)

# TFR multitaper transformation (EPOCHSTFR)
tfr = tfr_multitaper(combined_epochs, freqs=freqs, return_itc=False, verbose=True, time_bandwidth=2.0, n_cycles=freqs/2, average=False)
tfr_avgM = tfr.average()
tfr_avgM.plot(['Cz', 'C4', 'T8', 'CP6', 'CP2', 'FCz'], baseline=(-0.5, -0.2), mode='percent', title='auto', combine=None,
         tmin=-0.5, tmax=1, vmin=-0.6, vmax=0.6)
plt.show(block=False)

# TFR analysis and plotting for 0°C condition
tfr_0C = tfr_multitaper(combined_epochs['0°C'], freqs=freqs, return_itc=False, verbose=True, time_bandwidth=2.0, n_cycles=freqs/2)
tfr_0C.plot(['Cz'], baseline=(-0.5, -0.2), mode='percent', title='TFR for 0°C', combine=None, tmin=-0.5, tmax=1)
plt.show(block=False)

# TFR analysis and plotting for 10°C condition
tfr_10C = tfr_multitaper(combined_epochs['10°C'], freqs=freqs, return_itc=False, verbose=True, time_bandwidth=2.0, n_cycles=freqs/2)
tfr_10C.plot(['Cz'], baseline=(-0.5, -0.2), mode='percent', title='TFR for 10°C', combine=None, tmin=-0.5, tmax=1)
plt.show(block=False)

# TFR analysis and plotting for 18°C condition
tfr_18C = tfr_multitaper(combined_epochs['18°C'], freqs=freqs, return_itc=False, verbose=True, time_bandwidth=2.0, n_cycles=freqs/2)
tfr_18C.plot(['Cz'], baseline=(-0.5, -0.2), mode='percent', title='TFR for 18°C', combine=None, tmin=-0.5, tmax=1)
plt.show(block=False)

# TFR analysis and plotting for 22°C condition
tfr_22C = tfr_multitaper(combined_epochs['22°C'], freqs=freqs, return_itc=False, verbose=True, time_bandwidth=2.0, n_cycles=freqs/2)
tfr_22C.plot(['Cz'], baseline=(-0.5, -0.2), mode='percent', title='TFR for 22°C', combine=None, tmin=-0.5, tmax=1)
plt.show(block=False)



# TFR Morlet transformation
tfr = tfr_morlet(combined_epochs, freqs=freqs, n_cycles=freqs/2, return_itc=False, verbose=True, average=False)
tfr_avg = tfr.average()
tfr_avg.plot(['Cz', 'C4', 'T8', 'CP6', 'CP2', 'FCz'], baseline=(-0.5, -0.2), mode='percent', title='auto', combine=None,
         tmin=-0.5, tmax=1, vmin=-0.6, vmax=0.6)
plt.show(block=False)

# TFR Morlet transformation for 0°C condition
tfr_morlet_0C = tfr_morlet(combined_epochs['0°C'], freqs=freqs, n_cycles=freqs/2, return_itc=False, verbose=True, average=False)
tfr_avg_0C = tfr_morlet_0C.average()
tfr_avg_0C.plot(['Cz', 'C4', 'T8', 'CP6', 'CP2', 'FCz'], baseline=(-0.5, -0.2), mode='percent', title='auto', combine=None, tmin=-0.5, tmax=1, vmin=-0.6, vmax=0.6)
plt.show(block=False)

# TFR Morlet transformation for 10°C condition
tfr_morlet_10C = tfr_morlet(combined_epochs['10°C'], freqs=freqs, n_cycles=freqs/2, return_itc=False, verbose=True, average=False)
tfr_avg_10C = tfr_morlet_10C.average()
tfr_avg_10C.plot(['Cz', 'C4', 'T8', 'CP6', 'CP2', 'FCz'], baseline=(-0.5, -0.2), mode='percent', title='auto', combine=None, tmin=-0.5, tmax=1, vmin=-0.6, vmax=0.6)
plt.show(block=False)

# TFR Morlet transformation for 18°C condition
tfr_morlet_18C = tfr_morlet(combined_epochs['18°C'], freqs=freqs, n_cycles=freqs/2, return_itc=False, verbose=True, average=False)
tfr_avg_18C = tfr_morlet_18C.average()
tfr_avg_18C.plot(['Cz', 'C4', 'T8', 'CP6', 'CP2', 'FCz'], baseline=(-0.5, -0.2), mode='percent', title='auto', combine=None, tmin=-0.5, tmax=1, vmin=-0.6, vmax=0.6)
plt.show(block=False)

# TFR Morlet transformation for 22°C condition
tfr_morlet_22C = tfr_morlet(combined_epochs['22°C'], freqs=freqs, n_cycles=freqs/2, return_itc=False, verbose=True, average=False)
tfr_avg_22C = tfr_morlet_22C.average()
tfr_avg_22C.plot(['Cz', 'C4', 'T8', 'CP6', 'CP2', 'FCz'], baseline=(-0.5, -0.2), mode='percent', title='auto', combine=None, tmin=-0.5, tmax=1, vmin=-0.6, vmax=0.6)
plt.show(block=False)