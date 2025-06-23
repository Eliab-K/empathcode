#<<<<<<< HEAD
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mne
from scipy.signal import butter, lfilter, spectrogram
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

# Loop through each file in the folder
for file in file_list:
    file_path = os.path.join(folder_path, file)
    raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
    raw.set_montage("standard_1020", on_missing="ignore")
    data, sfreq = raw.get_data(), raw.info['sfreq']
    channels = raw.ch_names

    filtered_data = butter_bandpass_filter(data, 1, 40, sfreq)
    df_data = pd.DataFrame(filtered_data.T, columns=channels)

    print(f"\n📂 Processing EEG File: {file} ({len(channels)} channels)")

    # Compute band powers
    band_powers = {band: compute_band_power(filtered_data, sfreq, band_range) for band, band_range in BANDS.items()}
    band_powers_df = pd.DataFrame(band_powers)
    band_powers_df['channel'] = channels
    band_powers_df.set_index('channel', inplace=True)

   

    # Compute skewness and kurtosis
    stats_df = pd.DataFrame({
        'Skewness': [skew(filtered_data[ch]) for ch in range(filtered_data.shape[0])],
        'Kurtosis': [kurtosis(filtered_data[ch]) for ch in range(filtered_data.shape[0])],
    })
    stats_df['Channel'] = channels
    stats_df.set_index('Channel', inplace=True)

    # Plot skewness and kurtosis
    plt.figure(figsize=(14, 6))
    stats_df.plot(kind='bar', stacked=False)
    plt.title(f"Skewness & Kurtosis for EEG Channels ({file})", fontsize=16)
    plt.xlabel("Channel", fontsize=14)
    plt.ylabel("Statistical Value", fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.show()

    # Perform PCA and plot results
    pca = PCA(n_components=10)
    pca_results = pca.fit_transform(filtered_data.T)
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x=pca_results[:, 0], y=pca_results[:, 1])
    plt.title(f"PCA of EEG Data ({file})", fontsize=16)
    plt.xlabel("Principal Component 1", fontsize=14)
    plt.ylabel("Principal Component 2", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Perform t-SNE and plot results
    tsne = TSNE(n_components=2)
    tsne_results = tsne.fit_transform(filtered_data.T)
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x=tsne_results[:, 0], y=tsne_results[:, 1])
    plt.title(f"t-SNE of EEG Data ({file})", fontsize=16)
    plt.xlabel("Dimension 1", fontsize=14)
    plt.ylabel("Dimension 2", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Perform hierarchical clustering and plot dendrogram
    distance_matrix = pdist(filtered_data.T)
    linkage_matrix = linkage(distance_matrix, 'ward')
    plt.figure(figsize=(14, 8))
    dendrogram(linkage_matrix, labels=channels)
    plt.title(f"Hierarchical Clustering Dendrogram ({file})", fontsize=16)
    plt.xlabel("Channels", fontsize=14)
    plt.ylabel("Distance", fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
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
from scipy.signal import butter, lfilter, spectrogram
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

# Loop through each file in the folder
for file in file_list:
    file_path = os.path.join(folder_path, file)
    raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
    raw.set_montage("standard_1020", on_missing="ignore")
    data, sfreq = raw.get_data(), raw.info['sfreq']
    channels = raw.ch_names

    filtered_data = butter_bandpass_filter(data, 1, 40, sfreq)
    df_data = pd.DataFrame(filtered_data.T, columns=channels)

    print(f"\n📂 Processing EEG File: {file} ({len(channels)} channels)")

    # Compute band powers
    band_powers = {band: compute_band_power(filtered_data, sfreq, band_range) for band, band_range in BANDS.items()}
    band_powers_df = pd.DataFrame(band_powers)
    band_powers_df['channel'] = channels
    band_powers_df.set_index('channel', inplace=True)

   

    # Compute skewness and kurtosis
    stats_df = pd.DataFrame({
        'Skewness': [skew(filtered_data[ch]) for ch in range(filtered_data.shape[0])],
        'Kurtosis': [kurtosis(filtered_data[ch]) for ch in range(filtered_data.shape[0])],
    })
    stats_df['Channel'] = channels
    stats_df.set_index('Channel', inplace=True)

    # Plot skewness and kurtosis
    plt.figure(figsize=(14, 6))
    stats_df.plot(kind='bar', stacked=False)
    plt.title(f"Skewness & Kurtosis for EEG Channels ({file})", fontsize=16)
    plt.xlabel("Channel", fontsize=14)
    plt.ylabel("Statistical Value", fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.show()

    # Perform PCA and plot results
    pca = PCA(n_components=10)
    pca_results = pca.fit_transform(filtered_data.T)
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x=pca_results[:, 0], y=pca_results[:, 1])
    plt.title(f"PCA of EEG Data ({file})", fontsize=16)
    plt.xlabel("Principal Component 1", fontsize=14)
    plt.ylabel("Principal Component 2", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Perform t-SNE and plot results
    tsne = TSNE(n_components=2)
    tsne_results = tsne.fit_transform(filtered_data.T)
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x=tsne_results[:, 0], y=tsne_results[:, 1])
    plt.title(f"t-SNE of EEG Data ({file})", fontsize=16)
    plt.xlabel("Dimension 1", fontsize=14)
    plt.ylabel("Dimension 2", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Perform hierarchical clustering and plot dendrogram
    distance_matrix = pdist(filtered_data.T)
    linkage_matrix = linkage(distance_matrix, 'ward')
    plt.figure(figsize=(14, 8))
    dendrogram(linkage_matrix, labels=channels)
    plt.title(f"Hierarchical Clustering Dendrogram ({file})", fontsize=16)
    plt.xlabel("Channels", fontsize=14)
    plt.ylabel("Distance", fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.show()

    user_input = input("\n➡️ Press Enter to view the next file or type 'exit' to stop: ")
    if user_input.lower() == 'exit':
        print("📌 Stopping visualization.")
        break
>>>>>>> master
