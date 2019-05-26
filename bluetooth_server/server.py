from bluetooth import *
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

    try:
        #Loop that listen for a new message
        while True:
            msg = client_sock.recv(1024)
            if len(msg) == 0: break

            #Do actions depending on received message
            if(msg == "start"):
                # Tell respeaker thread to start listening sound

                #if all done right

                client_sock.send("done. [%s]." % msg)
                #else client_sock.send("error")
            elif(msg == "stop"):
                client_sock.send("done. [%s]." % msg)
            elif(msg.startswith('save')):
                tag = msg.split(" | ")[1]
                color = msg.split(" | ")[2]
                client_sock.send("done. [%s]." % msg)
            else:
                client_sock.send("received [%s]." % msg)
            print("received [%s]" % msg)

    except IOError:
        pass

    #disconnect and when for a new device
    print("disconnected")
    client_sock.close()

server_sock.close()
print("all done")
