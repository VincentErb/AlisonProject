# import alison.listen
from alison import Alison
import scipy.io.wavfile as wav
import numpy as np
import sys
import argparse
import json
import logging

alison = None


def learn_from_file(filename):
    global alison

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

            alison.add_dictionary_entry(tag, audio)


def on_receiving_audio(audio):
    global alison
    alison.process_audio(audio)

    for evt in alison.events:
        print("Recognized", evt.tag, "at time", evt.time, "with value",
              evt.value)

    alison.events.clear()


def plot_dictionary():
    import matplotlib.pyplot as plt
    global alison

    plt.figure(figsize=(7, 7))
    sizex = alison.components_per_tag
    sizey = alison.dictionary.shape[1] / sizex

    for i in range(0, alison.dictionary.shape[1]):
        plt.subplot(sizey, sizex, i + 1)
        plt.stem(alison.dictionary[:, i])

    plt.show()


def plot_nmf_results():
    import matplotlib.pyplot as plt
    global alison

    plt.figure(figsize=(7, 7))

    for i in range(0, alison.current_nmf_results.shape[0]):
        plt.subplot(6, 4, i + 1)
        plt.stem(alison.current_nmf_results[i, :])

    plt.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    alison = Alison()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        help="Recognize sound from an audio file instead of the ReSpeaker",
        type=str)
    parser.add_argument(
        "--learn",
        help="Name of a file that holds all the learning data",
        type=str)
    args = parser.parse_args()

    if args.learn != None:
        logging.info("Learn from file %s", args.learn)
        learn_from_file(args.learn)

    if args.file != None:
        logging.info("Input signal set to file %s", args.file)
        rate, signal = wav.read(args.file)
        on_receiving_audio(signal * 1.0)
    else:
        logging.info("Input signal set to ReSpeaker")
        # TODO Launch Respeaker thread
