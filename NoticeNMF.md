# Non-Negative Matrix Factorization
## Process

In order to recognize a known sound from the audio input we use the Non-Negative Matrix Factorization (NMF) algorithm. This algorithm decomposes the matrix given by the STFT in two matrices: the dictionnary and the activation matrix.

We make a dictionnary for each sound we want to recognize. We create the dictionnaries by computing NMF on the STFT of the concatenation of the sample of one sound.

When there is an audio input, we run a pattern matching algorithm based on the previously computed dictionnaries.
If the activation matrix contains coefficients above a certain threshold during a certain amount of time, we consider that the sound associated to this dictionnary is recognized.

Then a signal is sent to the Philips Hue to light it up in the pre-defined color.

## Diagram of the NMF method in the system process

![System Diagram](https://i.ibb.co/8NXwR6P/system.png)

## Testing

In order to test our programm, we made a dictionnary based on three different sounds we wanted to recognize. We recorded five samples for each sound.
After that, we tried to decompose complex sounds using the dictionnary we had created. Each coefficient in the decomposition tells us if and when the sound was recognized. 
We tested our algorithms with several sounds playing at the same time, recordings of sounds with noises and recordings without any learned sound.

## Properties

At the moment our algorithms manage to recognize superposed sounds and work in a noisy environnement. We can also recognize cut-up sounds (when there is only a part of the sound we want to recognise). We have some issues with false positive, meaning that we recognized sounds (especially doorbells) in a recording without sounds to recognize.
