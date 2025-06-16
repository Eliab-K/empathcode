import os  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mne
from scipy.signal import butter, lfilter
from scipy.stats import skew, kurtosis

# Enable interactive mode for better visualization (optional)
plt.ion()

# Path to EEG dataset
folder_path = r"C:\Users\Kahunde\OneDrive\Desktop\stress detector ml project\An EEG Recordings Dataset for Mental Stress Detection\An EEG Recordings Dataset for Mental Stress Detection\Complex Mathematical Problem solving (CMPS)"

if not os.path.exists(folder_path):
    raise FileNotFoundError(f'The folder does not exist')

file_list = [f for f in os.listdir(folder_path) if f.endswith('.edf')]

# Bandpass filter functions
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs  
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data, axis=1) 
    return y

# EEG Frequency Bands
BANDS = {
    'Delta': (0.5, 4),     
    'Theta': (4, 8),       
    'Alpha': (8, 13),
    'Beta': (13, 30),      
    'Gamma': (30, 40)     
}

# Compute band power
def compute_band_power(data, sfreq, band):
    lowcut, highcut = band
    filtered_data = butter_bandpass_filter(data, lowcut, highcut, sfreq)
    band_power = np.mean(filtered_data**2, axis=1)  
    return band_power

# Process EEG files
for file in file_list:
    file_path = os.path.join(folder_path, file)
    
    raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
    
    data, sfreq = raw.get_data(), raw.info['sfreq']
    channels = raw.ch_names

    filtered_data = butter_bandpass_filter(data, 1, 40, sfreq)

    # Debugging: Print shapes to ensure data consistency
    print(f"\n📂 Processing EEG File: {file} ({len(channels)} channels)")
    print(f"Filtered Data Shape: {filtered_data.shape}")

    # 1️⃣ Time Series EEG Plot (First 5 Channels)
    plt.figure(figsize=(12, 6))
    for ch in range(min(5, filtered_data.shape[0])):  
        plt.plot(filtered_data[ch, :], label=f'Channel {channels[ch]}')

    plt.title(f"Raw EEG Signals - {file}")
    plt.xlabel("Time (samples)")
    plt.ylabel("Amplitude (µV)")
    plt.legend()
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.show()

    # 2️⃣ Power Spectral Density (PSD) Plot (Fixed)
    info = mne.create_info(ch_names=channels, sfreq=sfreq, ch_types='eeg')
    filtered_raw = mne.io.RawArray(filtered_data, info)
    
    plt.figure(figsize=(12, 6))
    plt.title(f"Power Spectral Density (PSD) - {file}")
    filtered_raw.compute_psd().plot()
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.show()


    plt.figure(figsize=(10, 5))
    sns.histplot(filtered_data.flatten(), bins=50, kde=True)
    plt.title(f"EEG Signal Amplitude Distribution - {file}")
    plt.xlabel("Amplitude (µV)")
    plt.ylabel("Frequency")
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.show()


    plt.figure(figsize=(10, 5))
    sns.boxplot(data=filtered_data.T)
    plt.title(f"EEG Signal Amplitude Boxplot - {file}")
    plt.xlabel("Channel")
    plt.ylabel("Amplitude (µV)")
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.show()

    
    df_data = pd.DataFrame(filtered_data.T, columns=channels)
    corr_matrix = df_data.corr()

    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", xticklabels=channels, yticklabels=channels, square=True, linewidths=0.5)
    plt.title(f"EEG Channel Correlation Matrix - {file}")
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.show()

    # Pause for user input
    user_input = input("\n➡️ Press Enter to view the next file or type 'exit' to stop: ")
    if user_input.lower() == 'exit':
        print("📌 Stopping visualization.")
        break
