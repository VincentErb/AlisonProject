#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Script python pour Raspberry Pi.
Utilise le module bluetooth hc06 pour l'envoie et la reception de messages

Je ferais la version utilisant directement le bluetooth de la raspberry (si la raspberry pi que j'ai me laisse me connecter)

Les messages envoyés par l'application android se terminent toujours par un point à la fin
'''

import serial
import RPi.GPIO as GPIO

ser = serial.Serial('/dev/serial0', 9600)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(ledR,GPIO.OUT)
GPIO.setup(ledG,GPIO.OUT)
GPIO.setup(ledB,GPIO.OUT)

msg = ""
endMsg = false

def readMsg():
    global msg, endMsg
    while(ser.inWaiting() > 0):
        c = ser.read()
        if(c == '.'):
            endMsg = true
        else:
            msg += c

def handleMsg():
    global msg
    
    #format "listen sound | tag."
    if(msg.startswith('listen sound')):
        tag = msg.split(" | ")[1]
        # Signaler au thread du respeaker de démarrer l'enregistrement 
        #si ok retourner
        ser.write("ok")
        #sinon ser.write("error")
    elif(msg == "save sound"):
        #
        ser.write("ok")
    elif(msg == "etc"):
        #
        ser.write("ok")
    

while 1:
    readMsg()
    if(endMsg):
        handleMsg()
        endMsg = false
        msg = ""
    
