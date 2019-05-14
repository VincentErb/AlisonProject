import librosa
import librosa.display
import matplotlib.pyplot as plt

from alison.spectrum import *

# Plot spectrogram from STFT matrix
def plot_spectrogram(matrix):
    librosa.display.specshow(
        librosa.amplitude_to_db(matrix, ref=np.max),
        y_axis='log',
        x_axis='time')
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
        res[i] = ((i - 10) * 44100 / 1024)
    return res


# Basic test function
def test():
    path = "samples/Sonnette/sonnette1.wav"
    ma = get_stft_from_file(path)
    print(ma.shape)
    get_one_fft(ma)
    plot_spectrogram(ma)
    plot_fft(get_one_fft(ma))

if __name__ == "__main__":
    test()