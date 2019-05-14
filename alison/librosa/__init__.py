import warnings

import numpy as np
import scipy
import scipy.ndimage
import scipy.signal
import scipy.interpolate

#LOAD
import soundfile as sf
import audioread
import resampy

import six

from . import utils
from .utils import ParameterError

#FFT
__FFTLIB = None

def set_fftlib(lib=None):
    global __FFTLIB
    if lib is None:
        from numpy import fft
        lib = fft

    __FFTLIB = lib


def get_fftlib():
    global __FFTLIB
    return __FFTLIB


# Set the FFT library to numpy's, by default
set_fftlib(None)

#SFT
def stft(y, n_fft=2048, hop_length=None, win_length=None, window='hann',
         center=True, dtype=np.complex64, pad_mode='reflect'):

    # By default, use the entire frame
    if win_length is None:
        win_length = n_fft

    # Set the default hop, if it's not already specified
    if hop_length is None:
        hop_length = int(win_length // 4)

    fft_window = get_window(window, win_length, fftbins=True)

    # Pad the window out to n_fft size
    fft_window = utils.pad_center(fft_window, n_fft)

    # Reshape so that the window can be broadcast
    fft_window = fft_window.reshape((-1, 1))

    # Check audio is valid
    utils.valid_audio(y)

    # Pad the time series so that frames are centered
    if center:
        y = np.pad(y, int(n_fft // 2), mode=pad_mode)

    # Window the time series.
    y_frames = utils.frame(y, frame_length=n_fft, hop_length=hop_length)

    # Pre-allocate the STFT matrix
    stft_matrix = np.empty((int(1 + n_fft // 2), y_frames.shape[1]),
                           dtype=dtype,
                           order='F')

    fft = get_fftlib()

    # how many columns can we fit within MAX_MEM_BLOCK?
    n_columns = int(utils.MAX_MEM_BLOCK / (stft_matrix.shape[0] *
                                          stft_matrix.itemsize))

    for bl_s in range(0, stft_matrix.shape[1], n_columns):
        bl_t = min(bl_s + n_columns, stft_matrix.shape[1])

        stft_matrix[:, bl_s:bl_t] = fft.rfft(fft_window *
                                             y_frames[:, bl_s:bl_t],
                                             axis=0)
    return stft_matrix

def get_window(window, Nx, fftbins=True):
    if six.callable(window):
        return window(Nx)

    elif (isinstance(window, (six.string_types, tuple)) or
          np.isscalar(window)):
        # TODO: if we add custom window functions in librosa, call them here

        return scipy.signal.get_window(window, Nx, fftbins=fftbins)

    elif isinstance(window, (np.ndarray, list)):
        if len(window) == Nx:
            return np.asarray(window)

        raise ParameterError('Window size mismatch: '
                             '{:d} != {:d}'.format(len(window), Nx))
    else:
        raise ParameterError('Invalid window specification: {}'.format(window))

#----------------------LIBROSA.LOAD---------------------------------------------
def load(path, sr=22050, mono=True, offset=0.0, duration=None,
         dtype=np.float32, res_type='kaiser_best'):
    
    try:
        with sf.SoundFile(path) as sf_desc:
            sr_native = sf_desc.samplerate
            if offset:
                # Seek to the start of the target read
                sf_desc.seek(int(offset * sr_native))
            if duration is not None:
                frame_duration = int(duration * sr_native)
            else:
                frame_duration = -1

            # Load the target number of frames, and transpose to match librosa form
            y = sf_desc.read(frames=frame_duration, dtype=dtype, always_2d=False).T

    except RuntimeError as exc:
        # If soundfile failed, fall back to the audioread loader
        y, sr_native = __audioread_load(path, offset, duration, dtype)

    # Final cleanup for dtype and contiguity
    if mono:
        y = to_mono(y)

    if sr is not None:
        y = resample(y, sr_native, sr, res_type=res_type)

    else:
        sr = sr_native

    return y, sr

#necessary for load function
def __audioread_load(path, offset, duration, dtype):
    '''Load an audio buffer using audioread.
    This loads one block at a time, and then concatenates the results.
    '''

    y = []
    with audioread.audio_open(path) as input_file:
        sr_native = input_file.samplerate
        n_channels = input_file.channels

        s_start = int(np.round(sr_native * offset)) * n_channels

        if duration is None:
            s_end = np.inf
        else:
            s_end = s_start + (int(np.round(sr_native * duration))
                               * n_channels)

        n = 0

        for frame in input_file:
            frame = utils.buf_to_float(frame, dtype=dtype)
            n_prev = n
            n = n + len(frame)

            if n < s_start:
                # offset is after the current frame
                # keep reading
                continue

            if s_end < n_prev:
                # we're off the end.  stop reading
                break

            if s_end < n:
                # the end is in this frame.  crop.
                frame = frame[:s_end - n_prev]

            if n_prev <= s_start <= n:
                # beginning is in this frame
                frame = frame[(s_start - n_prev):]

            # tack on the current frame
            y.append(frame)

    if y:
        y = np.concatenate(y)
        if n_channels > 1:
            y = y.reshape((-1, n_channels)).T
    else:
        y = np.empty(0, dtype=dtype)

    return y, sr_native

def to_mono(y):
    # Validate the buffer.  Stereo is ok here.
    utils.valid_audio(y, mono=False)

    if y.ndim > 1:
        y = np.mean(y, axis=0)

    return y

def resample(y, orig_sr, target_sr, res_type='kaiser_best', fix=True, scale=False, **kwargs):
    # First, validate the audio buffer
    utils.valid_audio(y, mono=False)

    if orig_sr == target_sr:
        return y

    ratio = float(target_sr) / orig_sr

    n_samples = int(np.ceil(y.shape[-1] * ratio))

    if res_type in ('scipy', 'fft'):
        y_hat = scipy.signal.resample(y, n_samples, axis=-1)
    elif res_type == 'polyphase':
        if int(orig_sr) != orig_sr or int(target_sr) != target_sr:
            raise ParameterError('polyphase resampling is only supported for integer-valued sampling rates.')

        # For polyphase resampling, we need up- and down-sampling ratios
        # We can get those from the greatest common divisor of the rates
        # as long as the rates are integrable
        orig_sr = int(orig_sr)
        target_sr = int(target_sr)
        gcd = np.gcd(orig_sr, target_sr)
        y_hat = scipy.signal.resample_poly(y, target_sr // gcd, orig_sr // gcd, axis=-1)
    else:
        y_hat = resampy.resample(y, orig_sr, target_sr, filter=res_type, axis=-1)

    if fix:
        y_hat = utils.fix_length(y_hat, n_samples, **kwargs)

    if scale:
        y_hat /= np.sqrt(ratio)

    return np.ascontiguousarray(y_hat, dtype=y.dtype)

#UTIL



