import librosa as lib
import numpy as np

# MODULE TAKES AUDIO FILE PATH AS INPUT AND RETURNS FFT COEFFICIENTS OF A WINDOW OF THE SOUND


# Compute Short Term Fourier Transform (STFT) from an audio file path
# Returns a numpy matrix
def get_stft_from_file(wav):
    y, sample_rate = lib.load(wav)
    return get_stft(y)


def get_stft(data):
    # check data
    if type(data) != np.ndarray:
        data = np.array(data)

#    print("\ndata.ndim = " , data.ndim, "\t ", data, "\n")
    # try to detect 2 channel audio
    if data.ndim == 2:
        # keep only one channel
        #print("data ndim = [2]\n")
        data = data[0, :].flatten()

#    print("\ndata.ndim = " , data.ndim, "\t ", data, "\n")
    #if data == None or data == [] or data == np.ndarray(0) :
    #    print("\nwrong data format ", data, "\n")
    #    return None
    # Window size : 1024 -> around 47 ms, rather standard for FFT
    m = np.array([])
    if(data.size > 0):
        m = np.abs(lib.stft(data, n_fft=1024, window='hann'))
#    else:
#       print("\n\n returned NONE \n\n")
    return m


# Extracts one column of the STFT matrix
# Returns a numpy 1D-Array
def get_one_fft(stft):
    middle = int(stft.shape[1] / 2)
    return stft[:stft.shape[0], middle]


# Main primitive to use in main Alison module
# Input : audio file path
# Output : FFT frequency coefficients / 513 sized 1D-Array
def get_fft_from_audio(wav):
    stft = get_stft_from_file(wav)
    return get_one_fft(stft)
