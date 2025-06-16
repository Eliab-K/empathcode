<<<<<<< HEAD
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mne
from scipy.signal import butter, lfilter
from scipy.stats import skew, kurtosis

# Disable interactive mode
plt.ioff()

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

    # Plot the filtered data with adjusted y-axis for better readability
    plt.figure(figsize=(15, 10))
    for i, channel in enumerate(channels):
        plt.plot(filtered_data[i], label=channel)

    plt.title('Filtered EEG Data')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.ylim(-3000, 500)  # Adjust y-axis limits for better readability
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.tight_layout()
    plt.show(block=True)  # Keep the figure open until manually closed

    # Close the figure to free up memory
    plt.close()
=======
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mne
from scipy.signal import butter, lfilter
from scipy.stats import skew, kurtosis

# Disable interactive mode
plt.ioff()

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

    # Plot the filtered data with adjusted y-axis for better readability
    plt.figure(figsize=(15, 10))
    for i, channel in enumerate(channels):
        plt.plot(filtered_data[i], label=channel)

    plt.title('Filtered EEG Data')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.ylim(-3000, 500)  # Adjust y-axis limits for better readability
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.tight_layout()
    plt.show(block=True)  # Keep the figure open until manually closed

    # Close the figure to free up memory
    plt.close()
>>>>>>> master
