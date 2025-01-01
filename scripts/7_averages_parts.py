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

parts_average_all = {'0°C': [], '10°C': [], '18°C': [], '22°C': []}


for sub in subject_ids:

    plots_ica_save_file_name = 'cropped_drop_preprocessing-ica.fif'
    save_ICA_plots_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', 'cropped_drop_preprocessing-ica.fif')

    ica_save_file_name = 'cropped_preprocessing-ica.fif'
    save_ica_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', ica_save_file_name)

    epoched_save_file_name = 'cropped_epo.fif'
    save_epochs_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', epoched_save_file_name)

    save_file_name = 'cropped_filtered_raw.fif'
    save_file_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', save_file_name)

    evoked_save_file_name = 'cropped_evoked-ave.fif'
    save_evoked_path = os.path.join(save_path, 'sub-{}'.format(sub), 'eeg', evoked_save_file_name)



    # Loading data
    ica = mne.preprocessing.read_ica(save_ICA_plots_path)
    epochs = mne.read_epochs(save_epochs_path)

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


    # Habituation

    num_parts = 4
    epochs_per_part = len(epochs) // num_parts
    parts = []

    part_averages = {}
    for part in range(num_parts):
        start_idx = part * epochs_per_part
        end_idx = (part + 1) * epochs_per_part if part < num_parts - 1 else len(epochs)
        part_epochs = epochs[start_idx:end_idx]

        part_averages = {}  # Initialize the part-averages for this part
        for condition in conditions:
            part_avg = part_epochs[condition].average()
            part_averages[condition] = part_avg

        # Append the part-averages to the parts list
        parts.append(part_averages)

    part1 = parts[0]['0°C']
    part2 = parts[1]['0°C']
    part3 = parts[2]['0°C']
    part4 = parts[3]['0°C']

    evokeds_parted = {'Part 1': part1, 'Part 2': part2, 'Part 3': part3, 'Part 4': part4}
    mne.viz.plot_compare_evokeds(evokeds_parted, picks=['Cz'], title=f'Subject {sub} - Cz- 0°C')
    plt.show(block=True)

    part1 = parts[0]['10°C']
    part2 = parts[1]['10°C']
    part3 = parts[2]['10°C']
    part4 = parts[3]['10°C']

    evokeds_parted = {'Part 1': part1, 'Part 2': part2, 'Part 3': part3, 'Part 4': part4}
    mne.viz.plot_compare_evokeds(evokeds_parted, picks=['Cz'], title=f'Subject {sub} - Cz- 10°C')
    plt.show(block=True)

    part1 = parts[0]['18°C']
    part2 = parts[1]['18°C']
    part3 = parts[2]['18°C']
    part4 = parts[3]['18°C']

    evokeds_parted = {'Part 1': part1, 'Part 2': part2, 'Part 3': part3, 'Part 4': part4}
    mne.viz.plot_compare_evokeds(evokeds_parted, picks=['Cz'], title=f'Subject {sub} - Cz- 18°C')
    plt.show(block=True)

    part1 = parts[0]['22°C']
    part2 = parts[1]['22°C']
    part3 = parts[2]['22°C']
    part4 = parts[3]['22°C']

    evokeds_parted = {'Part 1': part1, 'Part 2': part2, 'Part 3': part3, 'Part 4': part4}
    mne.viz.plot_compare_evokeds(evokeds_parted, picks=['Cz'], title=f'Subject {sub} - Cz- 22°C')
    plt.show(block=True)


# Group-level plots

# Dictionaries
condition_averages_Cz = {'0°C': [], '10°C': [], '18°C': [], '22°C': []}

# Iterate through subjects and parts to compute condition averages
for sub in subject_ids:
    for part in parts:
        for condition in conditions:
            part_avg = part[condition]
            if 'Cz' in part_avg.info['ch_names']:
                condition_averages_Cz[condition].append(part_avg.pick_channels(['Cz']))

# Plot condition averages for Cz with separate lines for each part
for condition in conditions:
    evokeds = {f'Part {i + 1}': condition_averages_Cz[condition][i] for i in range(4)}
    mne.viz.plot_compare_evokeds(evokeds, picks='Cz',
                                 title=f'Cz {condition} Condition Averages',
                                 colors={'Part 1': '#d00000', 'Part 2': '#ffba08', 'Part 3': '#3f88c5', 'Part 4': '#032b43'}, ci=None)
    plt.show(block=True)

# Dictionaries
group_condition_averages_Cz = {'0°C': [], '10°C': [], '18°C': [], '22°C': []}

# Initialize the group averages lists for each condition
for condition in conditions:
    group_condition_averages_Cz[condition] = [None] * len(subject_ids)

# Iterate through subjects and parts to compute condition averages
for condition in conditions:
    for sub_idx, sub in enumerate(subject_ids):
        group_avg = None

        for part in parts:
            part_avg = part[condition]
            if 'Cz' in part_avg.info['ch_names']:
                if group_avg is None:
                    group_avg = part_avg
                else:
                    group_avg = mne.combine_evoked([group_avg, part_avg], weights='nave')

        group_condition_averages_Cz[condition][sub_idx] = group_avg


# Parts combined

# Dictionaries to store the averages
condition_averages_Cz = {'0°C': [], '10°C': [], '18°C': [], '22°C': []}

# Iterate through subjects and parts to compute condition averages
for sub in subject_ids:
    for part in parts:
        for condition in conditions:
            part_avg = part[condition]
            if 'Cz' in part_avg.info['ch_names']:
                condition_averages_Cz[condition].append(part_avg.pick_channels(['Cz']))

# Initialize dictionaries to store group-level averages
group_averages_Cz = {'Part 1': [], 'Part 1-2': [], 'Part 1-3': [], 'All Parts': []}

# Iterate through conditions
for condition in conditions:
    # Compute the group-level averages for each condition separately
    part_1_avg = sum([avg.data for avg in condition_averages_Cz[condition][:1]]) / len(condition_averages_Cz[condition][:1])
    part_1_2_avg = sum([avg.data for avg in condition_averages_Cz[condition][:2]]) / len(condition_averages_Cz[condition][:2])
    part_1_3_avg = sum([avg.data for avg in condition_averages_Cz[condition][:3]]) / len(condition_averages_Cz[condition][:3])
    all_parts_avg = sum([avg.data for avg in condition_averages_Cz[condition]]) / len(condition_averages_Cz[condition])

    # Create EvokedArray objects for the group-level averages
    info = condition_averages_Cz[condition][0].info
    part_1_avg_evoked = mne.EvokedArray(part_1_avg, info)
    part_1_2_avg_evoked = mne.EvokedArray(part_1_2_avg, info)
    part_1_3_avg_evoked = mne.EvokedArray(part_1_3_avg, info)
    all_parts_avg_evoked = mne.EvokedArray(all_parts_avg, info)

    # Store the group-level averages for each condition
    group_averages_Cz['Part 1'].append(part_1_avg_evoked)
    group_averages_Cz['Part 1-2'].append(part_1_2_avg_evoked)
    group_averages_Cz['Part 1-3'].append(part_1_3_avg_evoked)
    group_averages_Cz['All Parts'].append(all_parts_avg_evoked)

    # Plot condition averages for Cz with separate lines for each group-level average for the current condition
    evokeds = {key: group_averages_Cz[key][-1] for key in group_averages_Cz.keys()}
    colors = {'Part 1': '#d00000', 'Part 1-2': '#ffba08', 'Part 1-3': '#3f88c5', 'All Parts': '#032b43'}
    title = f'Cz {condition} Condition Averages'

    mne.viz.plot_compare_evokeds(evokeds, picks='Cz', title=title, colors=colors, ci=None)
    plt.show(block=True)