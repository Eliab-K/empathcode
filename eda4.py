<<<<<<< HEAD
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mne
from scipy.signal import butter, lfilter
from scipy.stats import skew, kurtosis
from sklearn.decomposition import PCA

# Set Seaborn style for better aesthetics
sns.set(style='whitegrid', context='talk')

# Path to EEG dataset
folder_path = r"C:\Users\Kahunde\OneDrive\Desktop\stress detector ml project\An EEG Recordings Dataset for Mental Stress Detection\An EEG Recordings Dataset for Mental Stress Detection\Complex Mathematical Problem solving (CMPS)"

if not os.path.exists(folder_path):
    raise FileNotFoundError(f'The folder does not exist')

file_list = [f for f in os.listdir(folder_path) if f.endswith('.edf')]

# Bandpass Filter Functions
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    return lfilter(b, a, data, axis=1)

# Frequency Bands
BANDS = {
    'Delta': (0.5, 4),
    'Theta': (4, 8),
    'Alpha': (8, 13),
    'Beta': (13, 30),
    'Gamma': (30, 40)
}

# Compute Band Power
def compute_band_power(data, sfreq, band):
    lowcut, highcut = band
    filtered_data = butter_bandpass_filter(data, lowcut, highcut, sfreq)
    return np.mean(filtered_data**2, axis=1)

# Processing Each EEG File
for file in file_list:
    file_path = os.path.join(folder_path, file)
    raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
    raw.set_montage("standard_1020", on_missing="ignore")  
    data, sfreq = raw.get_data(), raw.info['sfreq']
    channels = raw.ch_names

    # Bandpass Filtering
    filtered_data = butter_bandpass_filter(data, 1, 40, sfreq)
    df_data = pd.DataFrame(filtered_data.T, columns=channels)

    print(f"\n📂 Processing EEG File: {file} ({len(channels)} channels)")

    # Enhanced EEG Signal Visualization
    plt.figure(figsize=(16, 10))  # Larger figure size for clarity
    time = np.arange(0, data.shape[1]) / sfreq  # Time vector in seconds
    for i, channel in enumerate(channels):
        plt.plot(time, filtered_data[i], label=channel)
    
    plt.title(f"EEG Signals from {file}", fontsize=24, fontweight='bold')
    plt.xlabel("Time (s)", fontsize=20)
    plt.ylabel("Amplitude (µV)", fontsize=20)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(title="Channels", fontsize=14, title_fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.5)  # Add grid lines for clarity
    plt.tight_layout()
    plt.show()

    # Skewness and Kurtosis Calculation
    stats_df = pd.DataFrame({
        'Skewness': [skew(filtered_data[ch]) for ch in range(filtered_data.shape[0])],
        'Kurtosis': [kurtosis(filtered_data[ch]) for ch in range(filtered_data.shape[0])]
    })
    stats_df['Channel'] = channels
    stats_df.set_index('Channel', inplace=True)

    # Improved Skewness Visualization
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

    # Improved Kurtosis Visualization
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

    # PCA Visualization with Color Differentiation
    pca = PCA(n_components=2)
    pca_results = pca.fit_transform(filtered_data.T)

    # Example Classification Labels (Random for Demonstration)
    # Replace this with actual labels from your dataset
    labels = np.random.randint(0, 2, pca_results.shape[0])

    plt.figure(figsize=(12, 10))
    plt.scatter(pca_results[labels == 0, 0], pca_results[labels == 0, 1], 
                c='blue', alpha=0.7, edgecolors='k', label='Class 0')
    plt.scatter(pca_results[labels == 1, 0], pca_results[labels == 1, 1], 
                c='red', alpha=0.7, edgecolors='k', label='Class 1')
    plt.title(f"PCA of EEG Data ({file})", fontsize=24, fontweight='bold')
    plt.xlabel("Principal Component 1", fontsize=20)
    plt.ylabel("Principal Component 2", fontsize=20)
    plt.legend(title="Classes", title_fontsize=16, fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

    user_input = input("\n➡️ Press Enter to view the next file or type 'exit' to stop: ")
    if user_input.lower() == 'exit':
        print("📌 Stopping visualization.")
        break
=======
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mne
from scipy.signal import butter, lfilter
from scipy.stats import skew, kurtosis
from sklearn.decomposition import PCA

# Set Seaborn style for better aesthetics
sns.set(style='whitegrid', context='talk')

# Path to EEG dataset
folder_path = r"C:\Users\Kahunde\OneDrive\Desktop\stress detector ml project\An EEG Recordings Dataset for Mental Stress Detection\An EEG Recordings Dataset for Mental Stress Detection\Complex Mathematical Problem solving (CMPS)"

if not os.path.exists(folder_path):
    raise FileNotFoundError(f'The folder does not exist')

file_list = [f for f in os.listdir(folder_path) if f.endswith('.edf')]

# Bandpass Filter Functions
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    return lfilter(b, a, data, axis=1)

# Frequency Bands
BANDS = {
    'Delta': (0.5, 4),
    'Theta': (4, 8),
    'Alpha': (8, 13),
    'Beta': (13, 30),
    'Gamma': (30, 40)
}

# Compute Band Power
def compute_band_power(data, sfreq, band):
    lowcut, highcut = band
    filtered_data = butter_bandpass_filter(data, lowcut, highcut, sfreq)
    return np.mean(filtered_data**2, axis=1)

# Processing Each EEG File
for file in file_list:
    file_path = os.path.join(folder_path, file)
    raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
    raw.set_montage("standard_1020", on_missing="ignore")  
    data, sfreq = raw.get_data(), raw.info['sfreq']
    channels = raw.ch_names

    # Bandpass Filtering
    filtered_data = butter_bandpass_filter(data, 1, 40, sfreq)
    df_data = pd.DataFrame(filtered_data.T, columns=channels)

    print(f"\n📂 Processing EEG File: {file} ({len(channels)} channels)")

    # Enhanced EEG Signal Visualization
    plt.figure(figsize=(16, 10))  # Larger figure size for clarity
    time = np.arange(0, data.shape[1]) / sfreq  # Time vector in seconds
    for i, channel in enumerate(channels):
        plt.plot(time, filtered_data[i], label=channel)
    
    plt.title(f"EEG Signals from {file}", fontsize=24, fontweight='bold')
    plt.xlabel("Time (s)", fontsize=20)
    plt.ylabel("Amplitude (µV)", fontsize=20)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(title="Channels", fontsize=14, title_fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.5)  # Add grid lines for clarity
    plt.tight_layout()
    plt.show()

    # Skewness and Kurtosis Calculation
    stats_df = pd.DataFrame({
        'Skewness': [skew(filtered_data[ch]) for ch in range(filtered_data.shape[0])],
        'Kurtosis': [kurtosis(filtered_data[ch]) for ch in range(filtered_data.shape[0])]
    })
    stats_df['Channel'] = channels
    stats_df.set_index('Channel', inplace=True)

    # Improved Skewness Visualization
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

    # Improved Kurtosis Visualization
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

    # PCA Visualization with Color Differentiation
    pca = PCA(n_components=2)
    pca_results = pca.fit_transform(filtered_data.T)

    # Example Classification Labels (Random for Demonstration)
    # Replace this with actual labels from your dataset
    labels = np.random.randint(0, 2, pca_results.shape[0])

    plt.figure(figsize=(12, 10))
    plt.scatter(pca_results[labels == 0, 0], pca_results[labels == 0, 1], 
                c='blue', alpha=0.7, edgecolors='k', label='Class 0')
    plt.scatter(pca_results[labels == 1, 0], pca_results[labels == 1, 1], 
                c='red', alpha=0.7, edgecolors='k', label='Class 1')
    plt.title(f"PCA of EEG Data ({file})", fontsize=24, fontweight='bold')
    plt.xlabel("Principal Component 1", fontsize=20)
    plt.ylabel("Principal Component 2", fontsize=20)
    plt.legend(title="Classes", title_fontsize=16, fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

    user_input = input("\n➡️ Press Enter to view the next file or type 'exit' to stop: ")
    if user_input.lower() == 'exit':
        print("📌 Stopping visualization.")
        break
>>>>>>> master
