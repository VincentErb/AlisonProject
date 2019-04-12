from sklearn.decomposition import SparseCoder, NMF
import librosa.decompose as dcp
import scipy.io.wavfile as wav
import numpy as np


def get_nmf(stft, n_components):
    return dcp.decompose(stft, n_components=n_components)


def get_activations(stft, dico, n_nonzero_coefs=None):
    coder = SparseCoder(
        dictionary=dico.T,
        transform_n_nonzero_coefs=n_nonzero_coefs,
        transform_algorithm="omp")
    return coder.transform(stft.T).T


def test_sound_recognition():
    """
    Example on how to use get_nmf and get_activations
    """
    import matplotlib.pyplot as plt
    import learning

    rate, signal = wav.read("../samples/test0.wav")
    stft = learning.get_stft(signal / 1.0)

    for i in range(1, 5):
        if i == 2:
            continue

        rate, signal = wav.read("../samples/test" + str(i) + ".wav")
        stft = np.concatenate((stft, learning.get_stft(signal / 1.0)), axis=1)
        print(stft.shape)


    # obtain dictionary with NMF
    dico, base_act = get_nmf(stft, 32)

    rate2, signal2 = wav.read("../samples/door-bell01.wav")
    stft2 = learning.get_stft(signal / 1.0)

    # get activations using the previously computed dictionary
    # Here it's used on the same sound, but we can use it on different
    # sounds in order to classify them
    activations = get_activations(stft2, dico, 10)

    i = 50
    j = 50

    frame_act1 = base_act[:, i]
    frame_act2 = activations[:, j]

    plt.figure(figsize=(7, 7))
    plt.subplot(4, 2, 1)
    plt.title("Spectrum for sample a")
    plt.stem(stft[:, i])

    plt.subplot(4, 2, 2)
    plt.title("Spectrum for sample b")
    plt.stem(stft2[:, j])

    plt.subplot(4, 2, 3)
    plt.title("Reconstitution of sample b")
    plt.stem(np.dot(dico, frame_act2))

    plt.subplot(4, 2, 5)
    plt.title("Activations in the sample a")
    plt.stem(frame_act1)

    plt.subplot(4, 2, 6)
    plt.title("Activations found in sample b")
    plt.stem(frame_act2)

    main_activation1 = np.argsort(frame_act1)[-10:]
    main_activation2 = np.argsort(frame_act2)[-10:]

    plt.subplot(4, 2, 7)
    plt.title("Strongest feature identified in sample a")
    plt.stem(dico[:,main_activation1[-1]])

    plt.subplot(4, 2, 8)
    plt.title("Strongest feature identified in sample b")
    plt.stem(dico[:,main_activation2[-1]])

    print(main_activation1)
    print(frame_act1[main_activation1], "\n\n\n\n")
    print(main_activation2)
    print(frame_act2[main_activation2])

    print(np.intersect1d(main_activation1, main_activation2))

    plt.show()


def demo_nmf():
    """
    Show main components from nmf decomposition of an example sound
    """
    import matplotlib.pyplot as plt
    import learning

    # D = get_dictionnary(0).components_
    # print(D.shape)

    rate, signal = wav.read("../samples/door-bell01.wav")
    stft = learning.get_stft(signal[:, 0] / 1.0)
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
    test_sound_recognition()
