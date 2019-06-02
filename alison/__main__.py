import scipy.io.wavfile as wav
import numpy as np
import sys
import argparse
import json
import logging
import threading

from . import listen, mic_listener
from . import learn_from_file
from .recognition import SoundRecognizer
from . import philips_hue as lamps


def launch_bluetooth_server():
    import bluetooth_server


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        help="Recognize sound from an audio file instead of the ReSpeaker",
        type=str)
    parser.add_argument(
        "--learn",
        help="Name of a file that holds all the learning data",
        type=str)
    parser.add_argument(
        "--dict", help="Use a precomputed dictionary.", type=str)
    args = parser.parse_args()

    # Sink
    def callback(evt):
        print("Recognized", evt.tag, "at time", evt.time, "with value",
              evt.value)

    recognizer = SoundRecognizer(callback=callback)

    # Dict
    if args.dict != None:
        logging.info("Loading dictionary %s", args.dict)
        recognizer.load_dictionary(args.dict)

    # Learn
    if args.learn != None:
        logging.info("Learn from file %s", args.learn)
        learn_from_file(recognizer, args.learn)

    # Source
    if args.file != None:
        logging.info("Input signal set to file %s", args.file)
        rate, signal = read_wav_file(args.file)
        recognizer.process_audio(signal)
    else:
        logging.info("Input signal set to ReSpeaker")
        mic_listener = listen.MicListener(recognizer)

        logging.info("Starting bluetooth server thread")
        thread1 = threading.Thread(target=launch_bluetooth_server)
        thread1.start()

        mic_listener.run_listening()
