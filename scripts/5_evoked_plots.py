import os

import matplotlib.pyplot as plt
import mne
import numpy as np
import pandas as pd
import sklearn
import sys
from mne_bids import BIDSPath, read_raw_bids

# Paths
sub = '06'
save_path = '/data/pt_02697/eeg/pilot/data/lisa/processed_data_cold/'

plots_ica_save_file_name = 'drop_preprocessing-ica.fif'
save_ICA_plots_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', plots_ica_save_file_name)

epoched_save_file_name = '_epo.fif'
save_epochs_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', epoched_save_file_name)

save_file_name = 'filtered_raw.fif'
save_file_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', save_file_name)

# Loading data
ica = mne.preprocessing.read_ica(save_ICA_plots_path)
epochs = mne.read_epochs(save_epochs_path)
loaded_raw = mne.io.read_raw_fif(save_file_path)

# Montage
montage_file = '/data/gt_gr_eippert_cloud/Temp_sharing/lisa-marie/cfg/standard-10-5-cap385_added_mastoids (copy 3).elp'
montage = mne.channels.read_custom_montage(montage_file)
epochs.set_montage(montage)

# Evoked
evoked = epochs.average()

# Apply ICA to evoked data
evoked_ica = ica.apply(epochs).average()

# Evokeds
evokeds = dict(before_ica=evoked, after_ica=evoked_ica)

# Channels to plot
channels_to_plot = ['Cz', 'Fp2', 'T7', 'T8', 'O1']

# Plotting
for channel in channels_to_plot:
    mne.viz.plot_compare_evokeds(evokeds,
        picks=[channel],
        legend='upper left')
    plt.title(f'Evoked time course for channel {channel}')
    plt.show(block=True)


# Plots on a single figure
fig, axes = plt.subplots(len(channels_to_plot), 1, figsize=(8, 6), sharex=True)

for i, channel in enumerate(channels_to_plot):
    plot_info = {
        f'{channel}_before_ica': evoked.copy().pick_channels([channel]),
        f'{channel}_after_ica': evoked_ica.copy().pick_channels([channel])
    }

    mne.viz.plot_compare_evokeds(
        plot_info,
        picks=[channel],
        legend='upper right',
        show=False,
        axes=axes[i])

    axes[i].set_title(f'Evoked time course for channel {channel}')
    axes[i].tick_params(axis='both', labelsize='small')
    axes[i].grid(True)

plt.subplots_adjust(hspace=0.5)
plt.show()


# Thresholds
reject_criteria = dict(eeg=100e-6)
epochs.drop_bad(reject=reject_criteria)
epochs.plot_drop_log()

# Saving data

save_evoked_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', 'evoked-ave.fif')
evoked.save(save_evoked_path, overwrite=True)

save_epochs_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', 'preprocessed_epochs_epo.fif')
epochs.save(save_epochs_path, overwrite=True)