from bluetooth import *
#from alison import mic_listener
import subprocess


class BluetoothServer:
    def __init__(self, mic_listener):
        self.server_sock = BluetoothSocket(RFCOMM)
        self.server_sock.bind(("", PORT_ANY))
        self.server_sock.listen(1)
        self.port = self.server_sock.getsockname()[1]
        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        self.mic_listener = mic_listener

    def start(self):
        advertise_service(
            self.server_sock,
            "Alison_Project_Bluetooth_Server",
            service_id=self.uuid,
            service_classes=[self.uuid, SERIAL_PORT_CLASS],
            profiles=[SERIAL_PORT_PROFILE],
            #protocols = [ OBEX_UUID ]
        )
        print("Waiting for connection on RFCOMM channel %d" % self.port)

        #Wait for a device to connect to the server
        while True:
            client_sock, client_info = self.server_sock.accept()
            print("Accepted connection from ", client_info)

            current_audio = None

            try:
                #Loop that listen for a new message
                while True:
                    msg = client_sock.recv(1024)
                    if len(msg) == 0: break

                    msg = msg.decode("utf8")
                    #Do actions depending on received message
                    if (msg == "start"):
                        # Tell respeaker thread to start listening sound
                        print(type(self.mic_listener))
                        print(self.mic_listener)
                        self.mic_listener.start_learning()

                        #if all done right

                        client_sock.send("done. [%s]." % msg)
                        #else client_sock.send("error")
                    elif (msg == "stop"):
                        current_audio = self.mic_listener.stop_learning()

                        client_sock.send("done.")
                    elif (msg.startswith('save')):
                        tag = msg.split(" | ")[1]
                        color = msg.split(" | ")[2]

                        if current_audio != None:
                            self.mic_listener.register_sound(
                                tag, current_audio)
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

        self.server_sock.close()
        print("all done")
