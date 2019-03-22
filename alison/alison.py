
import numpy as np

class Event:
    def __init__(self, time, tag):
        self.time = time
        self.tag = tag

class Alison:
    def __init__(self):
        self.dictionary = []

        self.current_audio = []
        self.current_nmf_results = []
        self.events = []

    def add_dictionary_entry(self, entry):
        pass

    def process_audio(self, audio):
        """Compute spectrum from audio source, and call process_spectrum with the result"""
        pass

    def process_spectrum(self, spectrum):
        """Compute NMF and detect events from the results"""
        pass
