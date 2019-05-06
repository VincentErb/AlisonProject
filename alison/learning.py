#import librosa
#import librosa.display
import lib
import numpy as np
import matplotlib.pyplot as plt

# MODULE TAKES AUDIO FILE PATH AS INPUT AND RETURNS FFT COEFFICIENTS OF A WINDOW OF THE SOUND

# Compute Short Term Fourier Transform (STFT) from an audio file path
# Returns a numpy matrix
def get_stft_from_file(wav):
    y, sample_rate = lib.load(wav)
    return get_stft(y)

def get_stft(data):
    # Window size : 1024 -> around 47 ms, rather standard for FFT
    m = np.abs(lib.stft(data, n_fft=1024, window='hann'))
    return m

# Extracts one column of the STFT matrix
# Returns a numpy 1D-Array
def get_one_fft(stft):
    middle = int(stft.shape[1]/2)
    return stft[:stft.shape[0], middle]

# Main primitive to use in main Alison module
# Input : audio file path
# Output : FFT frequency coefficients / 513 sized 1D-Array
def get_fft_from_audio(wav):
    stft = get_stft_from_file(wav)
    return get_one_fft(stft)


# Plot spectrogram from STFT matrix
def plot_spectrogram(matrix):
    lib.display.specshow(lib.amplitude_to_db(matrix,
                                                     ref=np.max),
                             y_axis='log', x_axis='time')
    plt.title('Power spectrogram')
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    plt.show()

# Plots FFT from 1D-Array
# ATTENTION : shift in frequency UNSOLVED, not important ATM
def plot_fft(vector):
    y = vector.ravel()
    x = get_frequency_axis()
    print(y)
    plt.plot(x, y)
    plt.show()


# Sub-function used to plot_fft
def get_frequency_axis():
    res = np.empty(513)
    res[0] = 0
    res[1] = 2.1
    for i in range(10, 512):
        res[i] = ((i-10) * 44100 / 1024)
    return res


# Basic test function
def test():
    path = "../samples/door-bell01.wav"
    ma = get_stft_from_file(path)
    print(ma.shape)
    get_one_fft(ma)
    plot_spectrogram(ma)
    plot_fft(get_one_fft(ma))
