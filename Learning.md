# Registering new sounds

Any sound to be recognized by the system has to be recorded 4-5 times. The test samples are then treated to be used as dictionnary in the detection process.   
The following section refers to the python module : ```learning.py```

## Audio file treatement

We are using the Respeaker microphone to record a .WAV file from an input sound. The length of the recording is determined automatically by the Respeaker which stops recording when it detects the sound has stopped. Manual sound recording can be achieved using Respeaker's *record* function. 

## Feature extraction

NMF only requires the Fourier Transform of a sound to detect it, so the feature extraction process is rather simple.  
We load the .WAV file using Librosa*, and then compute the STFT (Short Term Fourier Transform) on the entire audio signal. This returns a 2D numpy array and the spectrogram obtained can be displayed in the learning module.

```python 
def get_stft_from_file(wav):
    y, sample_rate = librosa.load(wav)
    return get_stft(y)

def get_stft(data):
    # Window size : 1024 -> around 47 ms, rather standard for FFT
    m = np.abs(librosa.stft(data, n_fft=1024, window='hann'))
    return m
```

We used a standard Fourier Transform sampling rate, and a hanning window with overlapping to maintain information integrity.   
The matrix is then given to NMF to be used in the dictionnary matrix.





