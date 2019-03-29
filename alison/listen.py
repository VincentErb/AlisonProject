import time
import os
import wave
import struct
from respeaker import Microphone
from pixels import Pixels, pixels

LEN_AUDIO = 1 #in seconds
RATE = 16000
NUM = 1
LEN_DATA = int(LEN_AUDIO * RATE * 2)

def task():
    mic= Microphone()
    while 1:
        print("Listening\n")
        #pixels.listen()
        data=mic.listen(1,0.5)
        data=b''.join(data)
        #treat_data(data)
        record(data)

""" FUNCTION TO PAD DATA TO HAVE A CONSTANT SIZE
def treat_data(data):               

    last_index = len(data)-1        
    if len(data) == LEN_DATA:       #if the data is the right size
        print("Data is the right size "+str(len(data))+"\n")
        record(data)
    elif len(data) < LEN_DATA and len(data) != 0:      #if the data is too short
        print("Data is too small: padding "+str(len(data))+"\n")
        diff = LEN_DATA - len(data)
        packed_val = struct.pack('h',0)
        data2= data + ( (diff/2) * packed_val)
        record(data2)
    elif len(data) > LEN_DATA:      #if the data is too long
        print("Data is too big: cutting "+str(len(data))+"\n")
        data2 = data[0:(LEN_DATA-1)]
        data = data[LEN_DATA:last_index]
        record(data2)
        treat_data(data) 
"""

def record(data):
    global NUM
    
    if NUM < 10:
        name = '000'+str(NUM)
    elif NUM<100:
        name = '00'+str(NUM)
    elif NUM<1000:
        name = '0'+str(NUM)
        
    f = wave.open('/home/pi/Documents/Respeaker/TestWav/test'+name+'.wav','wb')
    f.setframerate(RATE)
    f.setsampwidth(2)
    f.setnchannels(1)
    f.writeframes(data)
    f.close
    NUM = NUM +1
    
def main():
    print('quit event')
    while True:
        try:
            task()
            print('waiting')
            time.sleep(1)
        except KeyboardInterrupt:
            print('Quit')
            break
    print('join')

if __name__ == '__main__':
    main()
