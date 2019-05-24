# Resources and Libraries

This project uses libraries to help with sound processing and signal analysis, mostly for NMF (Non-Negative-Matrix-Factorization).

## Respeaker

The Respeaker Project is a sound processing peripheral for Raspberry Pi. Hardware-wise, it includes 4 microphones allowing sound source localization. Software-wise, it helps with sound encoding and processing (it also provides advanced features like speech recognition that are not used in this project).
[Learn more about the Respeaker Project](https://respeaker.io/ "Respeaker")

We used the Respeaker to record .WAV files for new sound registering, and real time audio recording for the recognition process.

## LibROSA

Our main library is LibROSA. It is a well-known python signal processing tool that builds on sci-kit learn, another famous library. It helps us with everything that has to do with sound processing, including STFT's and NMF.
[More about LibROSA](https://librosa.github.io/librosa/ )


#### Raspberry Pi problems

While we installed every other library easily on our Raspberry Pi, dozens of hours of trial weren't enough for us to manage to insall LibROSA. LibROSA simply isn't meant for a Raspberry Pi processor. Fortunately, the methods used by Alison aren't the problematic ones in LibROSA.  
To solve the issue, we compiled our own mini version of LibROSA (the library is under ISC license, open to modifications) using only needed modules.

## PHue

Phue is a library designed to control Philips Hue lights through python. It is used to communicate sound class detection information in real time.   
[Get PHue](https://github.com/studioimaginaire/phue)


## Mkdocs

Documentation for the project, including this page, was generated thanks to Mkdocs, a static site generator from markdown. Custom theming has also been applied using mkdocs-material.  
[Learn more about Mkdocs](https://www.mkdocs.org)  
[Learn more about Mkdocs-material](https://squidfunk.github.io/mkdocs-material/)
