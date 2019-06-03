from bluetooth import *
from alison import mic_listener
import subprocess

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "Alison_Project_Bluetooth_Server",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
                   #protocols = [ OBEX_UUID ]
                    )
                   
print("Waiting for connection on RFCOMM channel %d" % port)

#Wait for a device to connect to the server
while True:
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)

    current_audio = None

    try:
        #Loop that listen for a new message
        while True:
            msg = client_sock.recv(1024)
            if len(msg) == 0: break
            msg = msg.decode("utf8")
            #Do actions depending on received message
            if(msg == "start"):
                # Tell respeaker thread to start listening sound
                print(type(mic_listener))
                print(mic_listener)
                mic_listener.start_learning()

                #if all done right

                client_sock.send("done. [%s]." % msg)
                #else client_sock.send("error")
            elif(msg == "stop"):
                current_audio = mic_listener.stop_learning()
                
                client_sock.send("done.")
            elif(msg.startswith('save')):
                tag = msg.split(" | ")[1]
                color = msg.split(" | ")[2]

                if current_audio != None:
                    mic_listener.register_sound(tag, current_audio)
                    client_sock.send("done.")
                else:
                    client_sock.send("error: no recording available.")
            else:
                client_sock.send("error: unknown message '%s'." % msg)
            print("received [%s]" % msg)

    except IOError:
        pass

    #disconnect and when for a new device
    print("disconnected")
    client_sock.close()

server_sock.close()
print("all done")
