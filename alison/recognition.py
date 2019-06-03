import numpy as np
import alison.nmf as nmf
from alison.spectrum import get_stft


class SoundEvent:
    def __init__(self, time, tag, value):
        self.time = time
        self.tag = tag
        self.value = value


class TagInfo:
    def __init__(self, components_range):
        self.components_range = components_range
        self.activated = False


class SoundRecognizer:
    def __init__(self, **kwargs):
        self.threshold = 10
        self.horizon = 20
        self.components_per_tag = 16
        # sample rate in hertz
        self.sample_rate = 25

        self.tags = {}
        # shape: [n_features, n_components]
        self.dictionary = None

        # current_audio contains the audio that was recorded but not yet parsed.
        self.current_position = 0
        self.current_audio = np.array([])
        # shape: [n_components, time]
        self.current_nmf_results = np.array([])

        # == Results
        # events are for example when a sound started to play
        self.events = []
        self.callback = kwargs["callback"] if "callback" in kwargs else None

    def _component_count(self):
        return self.dictionary.shape[1]

    def _reset_sound_processing(self):
        self.current_position = 0
        self.current_audio = np.array([])
        self.current_nmf_results = np.zeros([self._component_count(), 0])

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

    def save_dictionary(self, filename):
        """Save the dictionary to a file.
        Then the dictionary can be loaded with self.load_dictionary"""
        file = open(filename, 'w')
        file.write(str(self.dictionary.shape[0]))
        file.write(" ")
        file.write(str(self.dictionary.shape[1]))
        file.write("\n")

        file.write(str(len(self.tags)))
        file.write("\n")

        for key, value in self.tags.items():
            file.write(key.replace(" ", "_"))
            file.write(" ")
            file.write(str(value.components_range.start))
            file.write(" ")
            file.write(str(value.components_range.stop))
            file.write("\n")

        for l in range(0, self.dictionary.shape[0]):
            for c in range(0, self.dictionary.shape[1]):
                file.write(str(self.dictionary[l, c]))
                file.write(" ")

            file.write("\n")

        file.close()

    def load_dictionary(self, filename):
        """Load the dictionary from a file"""
        file = open(filename, 'r')
        lines = file.readlines()

        shapestr = lines[0].split(" ")
        self.dictionary = np.zeros([int(shapestr[0]), int(shapestr[1])])

        tag_count = int(lines[1])

        for i in range(0, tag_count):
            tag_str = lines[i + 2].split(" ")
            self.tags[tag_str[0]] = TagInfo(
                range(int(tag_str[1]), int(tag_str[2])))

        for l in range(0, self.dictionary.shape[0]):
            linestr = lines[l + 2 + tag_count].split(" ")

            for c in range(0, self.dictionary.shape[1]):
                self.dictionary[l, c] = float(linestr[c])

        self._reset_sound_processing()

    def process_audio(self, audio):
        """Compute spectrum from audio source, and call process_spectrum with
        the result"""
        self.current_audio = np.concatenate((self.current_audio, audio))
        spectrum = get_stft(self.current_audio)
        
        if spectrum.size > 0:
            self.process_spectrum(spectrum)

        # current functions parse the whole audio, so we let nothing in current_audio
        # (parsing the whole data regardless of its size, may result in artifacts
        # in the reconstructed spectrum)
        self.current_audio = np.array([])

    def process_spectrum(self, spectrum):
        """Compute NMF and detect events from the results.
        Mean is computed over `horizon` at each sample and the tag is activated if one
        of the components is greater than `threshold`"""
        if self.dictionary is None:
            return

        activations = nmf.get_activations(spectrum, self.dictionary)
        self.current_nmf_results = np.concatenate(
            (self.current_nmf_results, activations), axis=1)

        parsed_size = self.current_nmf_results.shape[1] - self.horizon

        for tag, tag_info in self.tags.items():
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
                        event = SoundEvent(
                            (self.current_position + i) / self.sample_rate,
                            tag, value)
                        self.events.append(event)

                        if self.callback != None:
                            self.callback(event)

        self.current_position += parsed_size
        self.current_nmf_results = self.current_nmf_results[:, -self.horizon:]
