# nmf.py
## Objectives

In order to recognise a known sound from the audio input we use the Non-Negative Matrix Factorization(NMF) algorithm. This algorithm decompose the matrix given by the STFT in two matrix : the dictionnary and the activation's matrix.

## Implementation
-----> To choose : We make a dictionnary for each sound we want to recognize or a dictionnary for all the sounds we want to recognize.

We create the dictionnaries by doing an NMF on the STFT of the concatenation of the sample sounds.

When there is an audio input we do one NMF for each dictionnary. If the coefficients in the activation's matrix of a sound are superior to a limit during a certain amount of time we consider that the sound is recognized.

A signal is then send to the Philipps Hue to light it up in the pre-define color.

## Testing

To test our theories we tried to recognize sounds loaded



## Properties

Noise ?
Superposition sound ?
Moving sound ?
Far away sound ?
