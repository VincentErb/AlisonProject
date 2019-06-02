import scipy.io.wavfile as wav
import numpy as np
import json

mic_listener = None


def read_wav_file(filename):
    """
    Read a wav file and return a tuple containing the signal and the sample rate.
    The signal is a one-dimensional numpy array of float containing raw values of
    the sound. This type of data is directly usable by the SoundRecognizer and other
    algorithms in Alison. 
    """
    rate, data = wav.read(filename)

    if type(data) != np.ndarray:
        data = np.array(data)

    # try to detect 2 channel audio
    if data.ndim == 2:
        # keep only one channel
        data = data[0, :].flatten()

    # TODO recognize 4 channel audio

    return rate, data * 1.0


def learn_from_file(recognizer, filename):
    with open(filename, 'r') as json_file:
        learn_data = json.load(json_file)

        for tag, files in learn_data.items():
            audio = np.array([])

            # TODO create a method to concatenate audio files
            for file in files:
                rate, signal = read_wav_file(file)
                audio = np.concatenate((audio, signal))

            recognizer.add_dictionary_entry(tag, audio)


def plot_dictionary(recognizer):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(7, 7))
    sizex = recognizer.components_per_tag
    sizey = recognizer.dictionary.shape[1] / sizex

    for i in range(0, recognizer.dictionary.shape[1]):
        plt.subplot(sizey, sizex, i + 1)
        plt.stem(recognizer.dictionary[:, i])

    plt.show()


def plot_nmf_results(recognizer):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(7, 7))

    for i in range(0, recognizer.current_nmf_results.shape[0]):
        plt.subplot(6, 4, i + 1)
        plt.stem(recognizer.current_nmf_results[i, :])

    plt.show()
