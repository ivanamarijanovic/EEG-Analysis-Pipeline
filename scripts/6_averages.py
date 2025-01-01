import os

import matplotlib.pyplot as plt
import mne
import numpy as np
import pandas as pd
import sklearn
import sys
from mne_bids import BIDSPath, read_raw_bids

# Paths
subject_ids = ['01', '02', '03', '04', '05', '06']
conditions = ['0°C', '10°C', '18°C', '22°C']
save_path = '/data/pt_02697/eeg/pilot/data/lisa/processed_data_cold/'

condition_averages_all = {'0°C': [], '10°C': [], '18°C': [], '22°C': []}
condition_averages_all_Fz = {'0°C': [], '10°C': [], '18°C': [], '22°C': []}

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


    # Loading data
    ica = mne.preprocessing.read_ica(save_ICA_plots_path)
    epochs = mne.read_epochs(save_epochs_path)
    epochs.crop(-0.5, 1)
    epochs = epochs.filter(l_freq = 1, h_freq = 45)

    # Montage
    montage_file = '/data/gt_gr_eippert_cloud/Temp_sharing/lisa-marie/cfg/standard-10-5-cap385_added_mastoids (copy 3).elp'
    montage = mne.channels.read_custom_montage(montage_file)
    epochs.set_montage(montage)

    loaded_raw = mne.io.read_raw_fif(save_file_path)
    evoked = mne.read_evokeds(save_evoked_path)

    # Interpolation
    raw_data_path = os.path.join(save_path, 'sub-06'.format(sub), 'eeg', save_file_name)
    raw = mne.io.read_raw_fif(raw_data_path, preload=True)


    raw.pick_channels(ch_names=[ch for ch in raw.ch_names if ch != 'T7'])
    raw.interpolate_bads()


    # Single-subject plots
    conditions = ['0°C', '10°C', '18°C', '22°C']

    # Time window
    tmin = -0.5
    tmax = 1.0

    epochs.crop(tmin, tmax)

    color_dict = {
        '0°C': '#5D5F71',
        '10°C': '#BF8B85',
        '18°C': '#DABECA',
        '22°C': '#E3D8F1'}

    condition_averages = {}
    for condition in conditions:
        condition_epochs = epochs[condition]
        condition_epochs_Fz = condition_epochs.copy().set_eeg_reference(['Fz'])
        baseline = (None, 0)
        condition_epochs.apply_baseline(baseline)
        condition_averages[condition] = condition_epochs.average()
        condition_averages_all[condition].append(condition_epochs.average())
        condition_averages_all_Fz[condition].append(condition_epochs_Fz.average())


    # Plot the condition averages
    mne.viz.plot_compare_evokeds(condition_averages, picks='Cz', title=f'Subject {sub} - Cz', colors=color_dict)
    plt.show(block=True)


    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for i, condition in enumerate(conditions):
        row, col = divmod(i, 2)
        ax = axes[row, col]
        condition_epochs = epochs[condition]
        baseline = (None, 0)
        condition_epochs.apply_baseline(baseline)

        mne.viz.plot_compare_evokeds({condition: condition_epochs.average()}, picks='Cz',
                                        title=f'Subject {sub} - Cz- {condition}', colors={condition: '#77BA99'},
                                        axes=ax)
    plt.show(block=True)




# Group-level plots
mne.viz.plot_compare_evokeds(condition_averages_all, picks='Cz',
                             title='Cz',
                             colors={'0°C': 'midnightblue', '10°C': 'royalblue', '18°C': 'deepskyblue',
                                     '22°C': 'paleturquoise'}, ci=None)
mne.viz.plot_compare_evokeds(condition_averages_all, picks='T8',
                             title='T8',
                             colors={'0°C': 'midnightblue', '10°C': 'royalblue', '18°C': 'deepskyblue',
                                     '22°C': 'paleturquoise'}, ci=None)
mne.viz.plot_compare_evokeds(condition_averages_all_Fz, picks='T8',
                             title='T8-Fz',
                             colors={'0°C': 'midnightblue', '10°C': 'royalblue', '18°C': 'deepskyblue',
                                     '22°C': 'paleturquoise'}, ci=None)
mne.viz.plot_compare_evokeds(condition_averages_all, picks='CP6',
                             title='CP6',
                             colors={'0°C': 'midnightblue', '10°C': 'royalblue', '18°C': 'deepskyblue',
                                     '22°C': 'paleturquoise'}, ci=True)
plt.show(block=True)


# Averaging
epochs.crop(-0.5, 1)

# General averages (all temps on different plots)

mne.viz.plot_compare_evokeds({'0°C': condition_averages_all['0°C']}, picks='Cz',
                                     title='Cz 0°C',
                                     colors={'0°C': 'midnightblue'})
mne.viz.plot_compare_evokeds({'0°C': condition_averages_all['0°C']},
                                     picks='T8', title='T8 0°C',
                                     colors={'0°C': 'midnightblue'})
mne.viz.plot_compare_evokeds({'0°C': condition_averages_all['0°C']},
                                     picks='CP6', title='CP6 0°C',
                                     colors={'0°C': 'midnightblue'})

mne.viz.plot_compare_evokeds({'10°C': condition_averages_all['10°C']}, picks='Cz',
                                     title='Cz 10°C',
                                     colors={'10°C': 'royalblue'})
mne.viz.plot_compare_evokeds({'10°C': condition_averages_all['10°C']},
                                     picks='T8', title='T8 10°C',
                                     colors={'10°C': 'royalblue'})
mne.viz.plot_compare_evokeds({'10°C': condition_averages_all['10°C']},
                                     picks='CP6', title='CP6 10°C',
                                     colors={'10°C': 'royalblue'})

mne.viz.plot_compare_evokeds({'18°C': condition_averages_all['18°C']}, picks='Cz',
                                     title='Cz  18°C',
                                     colors={'18°C': 'deepskyblue'})
mne.viz.plot_compare_evokeds({'18°C': condition_averages_all['18°C']},
                                     picks='T8', title='T8 18°C',
                                     colors={'18°C': 'deepskyblue'})
mne.viz.plot_compare_evokeds({'18°C': condition_averages_all['18°C']},
                                     picks='CP6', title='CP6 18°C',
                                     colors={'18°C': 'deepskyblue'})

mne.viz.plot_compare_evokeds({'22°C': condition_averages_all['22°C']}, picks='Cz',
                                     title='Cz 22°C',
                                     colors={'22°C': 'paleturquoise'})
mne.viz.plot_compare_evokeds({'22°C': condition_averages_all['22°C']},
                                     picks='T8', title='T8 22°C',
                                     colors={'22°C': 'paleturquoise'})
mne.viz.plot_compare_evokeds({'22°C': condition_averages_all['22°C']},
                                     picks='CP6', title='CP6 22°C',
                                     colors={'22°C': 'paleturquoise'})
plt.show(block=True)