# import alison.listen
from alison.alison import Alison

if __name__ == "__main__":
    alison = Alison()

    # listen.start_listening()

    while 1:
        audio = [] # listen.read_data() # <- this is a blocking function
        alison.process_audio(audio)

        for evt in alison.events:
            print("Recognized ", evt.tag, " at time ", evt.time)

        alison.events.clear()
