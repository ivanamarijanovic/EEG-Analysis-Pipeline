# EEG Analysis Pipeline

## Overview

This repository contains Python scripts for preprocessing and analyzing EEG data collected under various experimental conditions (0°C, 10°C, 18°C, 22°C). The project focuses on data quality improvement, artifact removal, and analysis of Event-Related Potentials (ERPs). The pipeline includes loading raw EEG data, signal enhancement, Independent Component Analysis (ICA), artifact rejection, and condition-specific analyses.

## Pipeline Description

### Preprocessing Steps
1. **Data Loading and Initial Inspection**:
   - Import raw EEG data and inspect initial characteristics.
   - Concatenate data from multiple runs.

2. **Signal Enhancement**:
   - High-pass filter (1 Hz): Removes slow signal drifts.
   - Low-pass filter (120 Hz): Preserves relevant frequencies up to 100 Hz.
   - Notch filter (50 Hz): Eliminates power line interference.

3. **Re-referencing**:
   - Signals are re-referenced to the average reference.

4. **Epoching and Quality Control**:
   - Segment continuous data into discrete time windows.
   - Perform manual rejection of problematic epochs (<5% per subject).

5. **Optimization**:
   - Downsample data to 500 Hz to reduce computational load.

6. **Independent Component Analysis (ICA)**:
   - Decomposes EEG data into independent components.
   - Identifies and removes components related to eye and muscle artifacts.

7. **Artifact Detection**:
   - Automatic rejection of epochs with amplitudes exceeding 100 µV.

---

### Analysis Workflow

1. **Time Window Selection**:
   - Focuses on a time window from -0.5 to 1 second relative to the event.

2. **Single-Subject Analysis**:
   - Computes average ERPs for each condition (0°C, 10°C, 18°C, 22°C).
   - Baseline correction is applied if necessary.

3. **Group-Level Analysis**:
   - Combines single-subject averages to compute group-level averages for each condition.

---

## Repository Structure

scripts/ - Contains Python scripts for each preprocessing and analysis step. 1_filtering.py - Performs filtering and signal enhancement. 2_resampling_epoching.py - Resamples data and segments it into epochs. 3_ICA.py - Runs Independent Component Analysis (ICA). 4_ICA_plots.py - Visualizes ICA components and artifact rejection. 5_evoked_plots.py - Generates evoked response plots. 6_averages.py - Computes condition-specific averages. 7_averages_parts.py - Analyzes data across experimental parts. 8_TFRs.py - Performs time-frequency analysis.


---

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/ivanamarijanovic/EEG-Analysis-Pipeline.git
   cd EEG-Analysis-Pipeline

    Install dependencies:

    pip install -r requirements.txt

    Run the scripts in order, starting from 1_filtering.py. Ensure that data paths and subject IDs are correctly configured.

Results

    Preprocessed Data:
        High-quality EEG signals with artifacts removed.
        Segmented and baseline-corrected epochs.

    Evoked Responses:
        Clear ERPs for each experimental condition (0°C, 10°C, 18°C, 22°C).
        Condition-specific and group-level averages.

    Time-Frequency Representations (TFRs):
        TFR plots highlighting power changes across conditions.
