import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt#for visualization
import seaborn as sns
import mne
from scipy.signal import butter, lfilter 
from scipy.stats import skew, kurtosis

folder_path = r"C:\Users\Kahunde\OneDrive\Desktop\stress detector ml project\An EEG Recordings Dataset for Mental Stress Detection\An EEG Recordings Dataset for Mental Stress Detection\Horrer Video Stimulation"

if not os.path.exists(folder_path):
  raise FileNotFoundError(f'The folder does not exist')

file_list = [f for f in os.listdir(folder_path) if f.endswith('.edf')]

  #processing EEG signals
def butter_bandpass(lowcut,highcut,fs, order=5):
    nyq = 0.5 * fs #Nyquist frequency
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low,high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data, axis=1) #applies filtering on time axis
    return y

eeg_signals = []
sampling_rates =[]
channel_names = []


  # Read all .edf files
for file in file_list:
    file_path = os.path.join(folder_path, file)
    
    # Read EEG data using MNE
    raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
    
    # Get EEG data and sampling frequency
    data, sfreq = raw.get_data(), raw.info['sfreq']
    channels = raw.ch_names
    filtered_data = butter_bandpass_filter(data, 1, 40, sfreq)
    
    eeg_signals.append(filtered_data)
    sampling_rates.append(sfreq)
    channel_names.append(channels)

plt.figure(figsize=(12, 8))
for ch in range(min(5, eeg_signals[0].shape[0])):  # Plot first 5 channels
    plt.plot(eeg_signals[0][ch, :], label=f'Channel {channel_names[0][ch]}')

plt.title("Raw EEG Signals (First 5 Channels)")
plt.xlabel("Time (samples)")
plt.ylabel("Amplitude (µV)")
plt.legend()
plt.show()

# Power Spectral Density (PSD) 
plt.figure(figsize=(12, 6))
plt.title("Power Spectral Density (PSD) - First File")
mne.viz.plot_raw_psd(mne.io.RawArray(eeg_signals[0], mne.create_info(ch_names=channel_names[0], sfreq=sampling_rates[0], ch_types='eeg')), show=False)
plt.show()

# Histogram of Amplitudes 
plt.figure(figsize=(10, 5))
sns.histplot(eeg_signals[0].flatten(), bins=50, kde=True)
plt.title("EEG Signal Amplitude Distribution")
plt.xlabel("Amplitude (µV)")
plt.ylabel("Frequency")
plt.show()

#Boxplots (Check for Outliers) 
plt.figure(figsize=(10, 5))
sns.boxplot(data=eeg_signals[0].T)
plt.title("EEG Signal Amplitude Boxplot")
plt.xlabel("Channel")
plt.ylabel("Amplitude (µV)")
plt.show()

#Statistical Feature Extraction 
feature_data = []
for signal in eeg_signals:
    mean_val = np.mean(signal, axis=1)
    std_val = np.std(signal, axis=1)
    min_val = np.min(signal, axis=1)
    max_val = np.max(signal, axis=1)
    median_val = np.median(signal, axis=1)
    rms_val = np.sqrt(np.mean(signal**2, axis=1))
    skewness_val = skew(signal, axis=1)
    kurtosis_val = kurtosis(signal, axis=1)

    # Store the average of all channels for each feature
    feature_data.append([
        np.mean(mean_val), np.mean(std_val), np.mean(min_val), np.mean(max_val),
        np.mean(median_val), np.mean(rms_val), np.mean(skewness_val), np.mean(kurtosis_val)
    ])

# Convert feature data to a DataFrame
df_features = pd.DataFrame(feature_data, columns=['Mean', 'Std', 'Min', 'Max', 'Median', 'RMS', 'Skewness', 'Kurtosis'])
print(df_features)

#Correlation Between EEG Channels 
corr_matrix = np.corrcoef(eeg_signals[0])  # Compute correlation for first EEG signal
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", xticklabels=channel_names[0], yticklabels=channel_names[0])
plt.title("EEG Channel Correlation Matrix")
plt.show()

