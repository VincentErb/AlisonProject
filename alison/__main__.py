import scipy.io.wavfile as wav
import numpy as np
import sys
import argparse
import json
import logging
import threading
import subprocess
import os
import _thread

from . import listen, mic_listener
from . import learn_from_file
from .recognition import SoundRecognizer
from . import philips_hue as lamps
from .server import BluetoothServer


def launch_bluetooth_server(mic_listener):
    bluetoothConServer = None

    def server_thread():
        bluetoothConServer.start()
        launch_bluetooth_server

    bluetoothConServer = BluetoothServer(mic_listener)
    thread1 = threading.Thread(target=server_thread)
    thread1.start()


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

    def kill_process(pid):
        res = os.popen("sudo kill -9 " + pid).read()
        #print("\n killed process [", pid, "] : res = [", res , "]\n")

    # Sink
    def callback(evt):
        print("Recognized", evt.tag, "at time", evt.time, "with value",
              evt.value)

        if (evt.tag == 'phone_ring'):
            _thread.start_new_thread(lamps.turn_on_alert, (3,1))
            #thread_light = threading.Thread(target=lamps.turn_on_alert(3,1))
            #thread_light.start()
           # proc = subprocess.Popen(
           #     ['python3', '/home/pi/4mics_hat/pixels_demo.py'],
           #     stdout=open("/home/pi/testzone/output.txt", "ab"))
           # threading.Timer(2, kill_process, [str(proc.pid)]).start()
        if (evt.tag == 'sonnette'):
            _thread.start_new_thread(lamps.turn_on_alert, (3,2))
        if (evt.tag == 'fire_alarm'):
            _thread.start_new_thread(lamps.turn_on_alert, (3,3))
            #thread_light = threading.Thread(target=lamps.turn_on_alert(3,2))
            #thread_light.start()
            #lamps.turn_on_alert(3,2)
            #proc = subprocess.Popen(
            #    ['python3', '/home/pi/4mics_hat/pixels.py'],
            #    stdout=open("/home/pi/testzone/output.txt", "ab"))
            #threading.Timer(2, kill_process, [str(proc.pid)]).start()

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
        launch_bluetooth_server(mic_listener)

        mic_listener.run_listening()
