import scipy.io.wavfile as wav
import numpy as np
import sys
import argparse
import json
import logging

from alison import learn_from_file, on_receiving_audio
from alison.recognition import SoundRecognizer
# import alison.listen


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    recognizer = SoundRecognizer()

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
        learn_from_file(recognizer, args.learn)

    if args.file != None:
        logging.info("Input signal set to file %s", args.file)
        rate, signal = wav.read(args.file)
        on_receiving_audio(recognizer, signal * 1.0)
    else:
        logging.info("Input signal set to ReSpeaker")
        # TODO Launch Respeaker thread
