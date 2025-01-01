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
ica_save_file_name = 'preprocessing-ica.fif'
save_ica_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', ica_save_file_name)

epoched_save_file_name = '_epo.fif'
save_epochs_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', epoched_save_file_name)

save_file_name = 'filtered_raw.fif'
save_file_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', save_file_name)

# Loading data
ica = mne.preprocessing.read_ica(save_ica_path)
epochs = mne.read_epochs(save_epochs_path)
loaded_raw = mne.io.read_raw_fif(save_file_path)

# Montage
montage_file = '/data/gt_gr_eippert_cloud/Temp_sharing/lisa-marie/cfg/standard-10-5-cap385_added_mastoids (copy 3).elp'
montage = mne.channels.read_custom_montage(montage_file)
epochs.set_montage(montage)


# Plot the data
epochs.average().detrend().plot_joint()

# EOG

eog_evoked = mne.preprocessing.create_eog_epochs(loaded_raw).average()
eog_evoked.apply_baseline(baseline=(None, -0.2))
eog_evoked.set_montage(montage)
eog_evoked.plot_joint()

# Find which ICs match the EOG pattern
eog_comp, eog_scores = ica.find_bads_eog(epochs)
ica.plot_scores(eog_scores, exclude = eog_comp, title='Component scores - EOG Rejection: ' + str(eog_comp)).show()


# Muscle artifacts

muscle_comp, muscle_scores = ica.find_bads_muscle(epochs)
ica.plot_scores(muscle_scores, exclude=muscle_comp, title='Component scores - Muscle Rejection: ' + str(muscle_comp)).show()
print(f"Automatically found muscle artifact ICA components: {muscle_comp}")

# Plots
ica.plot_sources(inst=epochs, show= True)

# Loop through all components and plot properties for each component

drop_idx = []
for comp in range(ica.n_components_):
    ica.plot_properties(epochs, picks=[comp])
    plt.show(block=True)
    drop = ""
    while not ((drop == 'y') or (drop =='n')):
        drop = input('Do you want to drop this component? (y/n)')
        if drop == 'y':
            drop_idx.append(comp)
        elif drop == 'n':
            pass
        else:
            print('Wrong input')

ica.exclude = drop_idx
ica.plot_sources(epochs, block=True)

# Apply ICA and plot the corrected epochs
ica.apply(epochs)


# Saving ICA_plots
save_ICA_plots_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', 'drop_preprocessing-ica.fif')
ica.save(save_ICA_plots_path, overwrite=True)