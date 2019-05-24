# Non-Negative Matrix Factorization
## Process

In order to recognize a known sound from the audio input we use the Non-Negative Matrix Factorization (NMF) algorithm. This algorithm decomposes the matrix given by the STFT in two matrices : the dictionnary and the activation matrix.

We make a dictionnary for each sound we want to recognize. We create the dictionnaries by computing NMF on the STFT of the concatenation of the sample of one sound.

When there is an audio input we run NMF once for each dictionnary (e.q each sound), if the coefficients in the activation's matrix are superior to a limit during a certain amount of time we consider that the sound corresponding to the dictionnary is recognized.

A signal is then send to the Philips Hue to light it up in the pre-defined color.

## Diagram of the NMF method in the system process

![System Diagram](https://i.ibb.co/8NXwR6P/system.png)

## Testing
[]
In order to test our programm we made a dictionnary for each sound from five samples of this sound. After we try to decompose complex sounds with the different dictionnaries. Each decomposition tell us if and when the sound is recognized. We tested our algorithms with several sounds playing at the same time, recording of sounds with noises and recording without sounds to recognized.

## Properties

For the moment our algorithms manage to recognize sounds in a superoposition of sounds or in a noisy environnement. We can also recognized cut-up sounds (when there is only a part of the sound we want to recognise). We have some issues with false positive, meaning that we recognized sounds (especially doorbells) in a recording without sounds to recognize.
