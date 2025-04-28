import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mne
from scipy.stats import skew, kurtosis

# Set Seaborn style for better aesthetics
sns.set(style='whitegrid', context='talk')

# Path to EEG dataset
folder_path = r"C:\Users\Kahunde\OneDrive\Desktop\stress detector ml project\An EEG Recordings Dataset for Mental Stress Detection\An EEG Recordings Dataset for Mental Stress Detection\Complex Mathematical Problem solving (CMPS)"

if not os.path.exists(folder_path):
    raise FileNotFoundError(f'The folder does not exist')

file_list = [f for f in os.listdir(folder_path) if f.endswith('.edf')]

# Processing each EEG file and calculating skewness and kurtosis
for file in file_list:
    file_path = os.path.join(folder_path, file)
    raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
    raw.set_montage("standard_1020", on_missing="ignore")  
    data, sfreq = raw.get_data(), raw.info['sfreq']
    channels = raw.ch_names

    # Skewness and Kurtosis Calculation
    skewness_values = [skew(data[ch]) for ch in range(data.shape[0])]
    kurtosis_values = [kurtosis(data[ch]) for ch in range(data.shape[0])]

    # Creating DataFrame for Skewness and Kurtosis
    stats_df = pd.DataFrame({
        'Skewness': skewness_values,
        'Kurtosis': kurtosis_values
    }, index=channels)

    # Skewness Visualization
    plt.figure(figsize=(14, 8))
    sns.barplot(x=stats_df.index, y='Skewness', data=stats_df, palette='viridis')
    plt.title(f'Skewness of EEG Channels ({file})', fontsize=22)
    plt.xlabel('EEG Channels', fontsize=18)
    plt.ylabel('Skewness', fontsize=18)
    plt.xticks(rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

    # Kurtosis Visualization
    plt.figure(figsize=(14, 8))
    sns.barplot(x=stats_df.index, y='Kurtosis', data=stats_df, palette='magma')
    plt.title(f'Kurtosis of EEG Channels ({file})', fontsize=22)
    plt.xlabel('EEG Channels', fontsize=18)
    plt.ylabel('Kurtosis', fontsize=18)
    plt.xticks(rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

    user_input = input("\n➡️ Press Enter to view the next file or type 'exit' to stop: ")
    if user_input.lower() == 'exit':
        print("📌 Stopping visualization.")
        break
