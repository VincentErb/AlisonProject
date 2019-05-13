import numpy as np
from learning import get_stft
import nmf


class AlisonEvent:
    def __init__(self, time, tag, value):
        self.time = time
        self.tag = tag
        self.value = value


class TagInfo:
    def __init__(self, components_range):
        self.components_range = components_range
        self.activated = False


class Alison:
    def __init__(self, **kwargs):
        self.threshold = 10
        self.horizon = 20
        self.components_per_tag = 8
        # sample rate in hertz
        self.sample_rate = 25

        self.tags = {}
        # shape: [n_features, n_components]
        self.dictionary = None

        # current_audio contains the audio that was recorded but not yet parsed.
        self.current_position = 0
        self.current_audio = []
        # shape: [n_components, time]
        self.current_nmf_results = []

        # == Results
        # events are for example when a sound started to play
        self.events = []

    def _component_count(self):
        return self.dictionary.shape[1]

    def _reset_sound_processing(self):
        self.current_position = 0
        self.current_audio = []
        self.current_nmf_results = np.zeros([self._component_count(), 9])

        self.events = []

    def add_dictionary_entry(self, tag, entry):
        """Add a sound to be recognized by Big Alison.
        
        entry: a sound sample containing mostly the sound to recognize."""
        stft = get_stft(entry)
        dico, _ = nmf.get_nmf(stft, self.components_per_tag)

        if self.dictionary is None:
            self.dictionary = dico
        else:
            self.dictionary = np.concatenate((self.dictionary, dico), axis=1)

        range_stop = self.dictionary.shape[1]
        range_start = range_stop - dico.shape[1]
        self.tags[tag] = TagInfo(range(range_start, range_stop))
        self._reset_sound_processing()

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
        """Compute NMF and detect events from the results.
        Mean is computed over `horizon` at each sample and the tag is activated if one
        of the components is greater than `threshold`"""
        activations = nmf.get_activations(spectrum, self.dictionary)
        self.current_nmf_results = np.concatenate(
            (self.current_nmf_results, activations), axis=1)

        parsed_size = self.current_nmf_results.shape[1] - self.horizon

        for tag, tag_info in self.tags.items():
            print(tag)
            for i in range(parsed_size):
                tag_range = tag_info.components_range
                results = np.percentile(
                    self.current_nmf_results[tag_range.start:tag_range.stop, i:
                                             (i + self.horizon)],
                    70,
                    axis=1)
                value = np.percentile(results, 70)
                activated = value > self.threshold

                if tag_info.activated != activated:
                    tag_info.activated = activated

                    if tag_info.activated:
                        self.events.append(
                            AlisonEvent(
                                (self.current_position + i) / self.sample_rate,
                                tag, value))

        self.current_position += parsed_size
        # self.current_nmf_results = self.current_nmf_results[:, :-self.horizon]
