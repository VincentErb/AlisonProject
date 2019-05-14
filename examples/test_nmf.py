import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt

import alison.spectrum as spectrum
from alison.nmf import *


def test_sound_recognition_v2():
    files = [
        "samples/Sonnette/sonnette", "samples/Fire_Alarm/fire_alarm",
        "samples/Phone_Ring/phone"
    ]

    dico = np.zeros([513, 0])
    print(dico.shape)

    for file in files:
        stft = np.zeros([513, 0])

        for i in range(1, 5):
            rate, signal = wav.read(file + str(i) + ".wav")
            stft = np.concatenate((stft, spectrum.get_stft(signal / 1.0)),
                                  axis=1)

        dico_plus, _ = get_nmf(stft, 3)
        dico = np.concatenate((dico, dico_plus), axis=1)

    for file in files:
        rate2, signal2 = wav.read(file + "5.wav")
        stft2 = spectrum.get_stft(signal2 * 1.0)
        activations = get_activations(stft2, dico, 3)

        plt.clf()

        for i in range(0, 9):
            plt.subplot(3, 3, i + 1)
            plt.title("Ligne " + str(i))
            plt.stem(activations[i, :])

        plt.show()


def test_sound_recognition():
    """
    Example on how to use get_nmf and get_activations
    """

    rate, signal = wav.read("samples/Sonnette/sonnette1.wav")
    stft = spectrum.get_stft(signal * 1.0)

    for file in [
            "samples/Sonnette/sonnette", "samples/Fire_Alarm/fire_alarm",
            "samples/Phone_Ring/phone"
    ]:

        for i in range(1, 5):

            rate, signal = wav.read(file + str(i) + ".wav")
            stft = np.concatenate((stft, spectrum.get_stft(signal / 1.0)),
                                  axis=1)

    print(stft.shape)

    # obtain dictionary with NMF
    dico, base_act = get_nmf(stft, 8)

    rate2, signal2 = wav.read("samples/Sonnette/sonnette5.wav")
    stft2 = spectrum.get_stft(signal2 * 1.0)

    # get activations using the previously computed dictionary
    # Here it's used on the same sound, but we can use it on different
    # sounds in order to classify them
    activations = get_activations(stft2, dico, 3)

    i = 100
    j = 100

    frame_act1 = base_act[:, i]
    frame_act2 = activations[:, j]

    plt.figure(figsize=(7, 7))
    plt.subplot(3, 2, 1)
    plt.title("Spectrum for sample a")
    plt.stem(stft[:, i])

    plt.subplot(3, 2, 2)
    plt.title("Spectrum for sample b")
    plt.stem(stft2[:, j])

    plt.subplot(3, 2, 3)
    plt.title("Reconstitution of sample b")
    plt.stem(np.dot(dico, frame_act2))

    plt.subplot(3, 2, 4)
    plt.title("Ligne 1")
    plt.stem(activations[0, :])

    plt.subplot(3, 2, 5)
    plt.title("Ligne 2")
    plt.stem(activations[1, :])

    plt.subplot(3, 2, 6)
    plt.title("Ligne 3")
    plt.stem(activations[2, :])

    plt.show()


def demo_nmf():
    """
    Show main components from nmf decomposition of an example sound
    """

    # D = get_dictionnary(0).components_
    # print(D.shape)

    rate, signal = wav.read("samples/door-bell01.wav")
    stft = spectrum.get_stft(signal[:, 0] / 1.0)
    components, activation = dcp.decompose(stft)

    i = 0
    # first frame spectrum
    spectrum = stft[:, i]
    # first frame component activation
    line = activation[:, i]

    # Extract spectrum for the 4 strongest activation on the first frame
    ind = np.argsort(line)[-4:]
    maincomps = components[:, ind]

    # Plot
    plt.figure(figsize=(7, 7))

    plt.subplot(6, 1, 1)
    plt.title("Spectrum")
    plt.stem(spectrum)

    plt.subplot(6, 1, 2)
    plt.title("Components")
    plt.stem(line)

    for n in range(4):
        plt.subplot(6, 1, n + 3)
        plt.stem(maincomps[:, n])

    plt.show()


if __name__ == "__main__":
    test_sound_recognition_v2()
