import time
import os
import wave
import struct
import threading
import os

from respeaker import Microphone
from spectrum import *

LEN_AUDIO = 1  #in seconds
RATE = 16000
#NUM = 1
LEN_DATA = int(LEN_AUDIO * RATE * 2)


class MicListener:
    learning = False
    learning_recording = None

    end_learning_event = threading.Event()
    recognizer_lock = threading.RLock()

    def __init__(self, recognizer):
        self.recognizer = recognizer

    def run_listening(self):
        mic = Microphone()

        try:
            while 1:
                print("Listening\n")
                was_learning = self.learning
                data = mic.listen(LEN_AUDIO, 1)  #make recordings of one second
                data = b''.join(data)

                if was_learning:
                    self.learning_recording += data

                    if not self.learning:
                        self.end_learning_event.set()
                else:
                    self.recognizer_lock.acquire()
                    self.recognizer.process_audio(data)
                    self.recognizer_lock.release()

                    if self.learning:
                        self.end_learning_event.clear()

        except KeyboardInterrupt:
            print("Quit")

    def start_learning(self):
        """
        Start recording a sound for learning purpose. 
        """
        self.learning_recording = None
        self.learning = True

    def stop_learning(self):
        """
        Stop recording a sound for learning purpose and returns the recorded
        sample.
        """
        self.learning = False
        self.end_learning_event.wait()
        return self.learning_recording

    def register_sound(self, name, audio):
        self.recognizer_lock.acquire()
        self.recognizer.add_dictionary_entry(name, audio)
        self.recognizer_lock.release()

    def save_file(self, name, data):
        """
        Save the data as a file in the current directory.
        """
        path = os.getcwd() + '/' + name + '.wav'

        #path = '/home/pi/Documents/Respeaker/TestWav/test'+str(i)+'.wav'

        # print("Launching Thread " + str(i))
        #Save raw data as wave file
        f = wave.open(path, 'wb')
        f.setframerate(RATE)
        f.setsampwidth(2)
        f.setnchannels(1)
        f.writeframes(data)
        f.close()

        #Call SFT function
        sft = get_stft_from_file(path)
        #print(sft.shape)
        #print(get_one_fft(sft))

        #destroy the created file
        """
        if os.path.exists(path):
            os.remove(path)
        else:
            print("The file does not exist")
        """


if __name__ == '__main__':
    # MicListener(None).run_listening()
    pass
