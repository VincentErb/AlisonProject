import numpy as np
from alison.learning import get_stft


class Event:
    def __init__(self, time, tag):
        self.time = time
        self.tag = tag


class Alison:
    def __init__(self):
        self.dictionary = []

        # current_audio contains the audio that was recorded but not yet parsed.
        self.current_audio = []
        self.current_nmf_results = []
        self.events = []

    def add_dictionary_entry(self, entry):
        pass

    def process_audio(self, audio):
        """Compute spectrum from audio source, and call process_spectrum with
        the result"""
        self.current_audio.append(audio)
        spectrum = get_stft(self.current_audio)
        self.process_spectrum(spectrum)

        # current functions parse the whole audio, so we let nothing in current_audio
        # (parsing the whole data regardless of its size, may result in artifacts
        # in the reconstructed spectrum)
        self.current_audio.clear()

    def process_spectrum(self, spectrum):
        """Compute NMF and detect events from the results"""
        pass
