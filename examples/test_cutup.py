import os

from alison import read_wav_file
from alison.recognition import SoundRecognizer

recognizer = None

def reset_recognizer():
    global recognizer
    recognizer = SoundRecognizer(callback=callback)
    recognizer.load_dictionary("samples/sample.dict")

if __name__ == "__main__":
    def callback(evt):
        print("Recognized", evt.tag, "at time", evt.time, "with value",
              evt.value)
    
    reset_recognizer()
    
    directory = "./samples/Cut_Up_Sounds/other_Fire_Alarm/"
    files = os.listdir(directory)
    files.sort()
    
    print(" - Processing with reset")
    
    for file in files:
        print(file)
        
        if file.endswith(".wav"):
            _, signal = read_wav_file(directory + file)
            recognizer.process_audio(signal)
            reset_recognizer()
    
    print(" - Processing without reset")
    
    for file in files:
        print(file)
        
        if file.endswith(".wav"):
            _, signal = read_wav_file(directory + file)
            recognizer.process_audio(signal)
    
    
    