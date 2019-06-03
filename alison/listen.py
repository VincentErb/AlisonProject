import time
import os
import wave
import struct
import threading
import _thread
import os

from . import read_wav_file

from respeaker import Microphone

LEN_AUDIO = 1  #in seconds
RATE = 16000
# NUM = 1
LEN_DATA = int(LEN_AUDIO * RATE * 2)


class MicListener:
    learning = False
    learning_recording = None
    file_id = 0

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
                    _thread.start_new_thread(self.process_audio, (data))

                    if self.learning:
                        self.end_learning_event.clear()

        except KeyboardInterrupt:
            print("Quit")

    def convert_audio(self, data):
        """
        Convert respeaker data to audio 
        """
        filename = str(self.file_id)
        self.save_file(filename, data)
        rate, signal = read_wav_file(filename + ".wav")
        self.delete_file(filename)
        self.file_id += 1
        return rate, signal

    def process_audio(self, data):
        rate, signal = self.convert_audio(data)

        self.recognizer_lock.acquire()
        self.recognizer.process_audio(signal)
        self.recognizer_lock.release()

    def start_learning(self):
        """
        Start recording a sound for learning purpose. 
        """
        self.learning_recording = b''
        self.learning = True

    def stop_learning(self):
        """
        Stop recording a sound for learning purpose and return the recorded
        sample.
        """
        self.learning = False
        self.end_learning_event.wait()
        rate, audio = self.convert_audio(self.learning_recording)
        return audio

    def register_sound(self, name, audio):
        self.recognizer_lock.acquire()
        self.recognizer.add_dictionary_entry(name, audio)
        self.recognizer_lock.release()

    def save_file(self, name, data):
        """
        Save the data as a file in the current directory.
        """
        global RATE

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
        #print(sft.shape)
        #print(get_one_fft(sft))

    def delete_file(self, name):
        path = os.getcwd() + '/' + name + '.wav'
        #destroy the created file
        if os.path.exists(path):
            os.remove(path)
        else:
            print("The file does not exist")


if __name__ == '__main__':
    # MicListener(None).run_listening()
    pass
