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
                rate, signal = wav.read(args.file)
                signal = np.array(signal)
                
                if signal.ndim == 2:
                    signal = signal[0, :].flatten()
                
                audio = np.concatenate((audio, signal))
            
            alison.add_dictionary_entry(tag, audio)


def on_receiving_audio(audio):
    global alison
    alison.process_audio(audio)

    for evt in alison.events:
        print("Recognized ", evt.tag, " at time ", evt.time)

    alison.events.clear()


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
