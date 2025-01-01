import os

import matplotlib.pyplot as plt
import mne
import numpy as np
import pandas as pd
from mne_bids import BIDSPath, read_raw_bids

subjects = ['06']
n_runs = 4
task = 'thermal'
data_path = '/data/pt_02697/eeg/pilot/data/lisa/raw_data_cold/'
save_path = '/data/pt_02697/eeg/pilot/data/lisa/processed_data_cold/'
sr_new = 500
filter_type = 'FIR'



for sub in subjects:
    if not os.path.isdir(os.path.join(save_path, 'sub-{}'.format(sub), 'eeg')):
        os.makedirs(os.path.join(save_path, 'sub-{}'.format(sub), 'eeg'))

    raw = []
    event_files = []
    for i in range(n_runs):
        run = i + 1   #get correct run number
        bids_path = BIDSPath(subject=sub, run=run, task=task, root=data_path)
        data = read_raw_bids(bids_path=bids_path, extra_params={'preload': True})
        raw.append(data)

        event_file = pd.read_csv(os.path.join(data_path, 'sub-{}'.format(sub), 'eeg', 'sub-{0}_task-{1}_run-0{2}_events.tsv'.format(sub, task, run)), sep='\t')
        event_files.append(event_file)

    if sub == 'pilot02':        #only used in early pilots
        raw[4].drop_channels(['STI 015'])


# merge files
raw = mne.concatenate_raws(raw)
montage_file = '/data/gt_gr_eippert_cloud/Temp_sharing/lisa-marie/cfg/standard-10-5-cap385_added_mastoids (copy 3).elp'
montage = mne.channels.read_custom_montage(montage_file)
raw.set_montage(montage)
raw.compute_psd(fmax=160).plot()
raw.plot(duration=10, scalings="auto", title="Raw EEG data")
plt.show(block=True)
raw.set_eeg_reference(ref_channels='average')

# filtering
raw_filtered = raw.copy()
raw_filtered.filter(l_freq=1, h_freq=120)

# plotting
raw.plot(duration=10, scalings="auto", title="Raw EEG data")

raw_filtered.plot(duration=10, scalings="auto", title="Filtered EEG data")

plt.show(block=True)


# PSD

raw_filtered.compute_psd(fmax=160).plot()

# Notch filter

raw_filtered.notch_filter(freqs=50)

raw_filtered.compute_psd(fmax=160).plot()

plt.show(block=True)

# Save the filtered raw data
save_file_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', 'filtered_raw.fif')
raw_filtered.save(save_file_path, overwrite=True)
