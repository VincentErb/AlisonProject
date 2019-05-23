import scipy.io.wavfile as wav
import numpy as np
import json

mic_listener = None


def learn_from_file(recognizer, filename):
    with open(filename, 'r') as json_file:
        learn_data = json.load(json_file)

        for tag, files in learn_data.items():
            audio = np.array([])

            # TODO create a method to concatenate audio files
            for file in files:
                rate, signal = wav.read(file)
                signal = np.array(signal)

                if signal.ndim == 2:
                    signal = signal[0, :].flatten()

                audio = np.concatenate((audio, signal))

            recognizer.add_dictionary_entry(tag, audio)


def on_receiving_audio(recognizer, audio):
    recognizer.process_audio(audio)

    for evt in recognizer.events:
        print("Recognized", evt.tag, "at time", evt.time, "with value",
              evt.value)

    recognizer.events.clear()


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
