import numpy as np
from scipy.io import wavfile
import sounddevice as sd

def load_wav_file(filepath):
    samplerate, data = wavfile.read(filepath)

    # Convert stereo to mono
    if len(data.shape) == 2:
        data = data.mean(axis=1).astype(np.int16)

    # Force to int16 format
    if data.dtype != np.int16:
        data = data.astype(np.int16)

    return samplerate, data

def save_wav_file(filepath, samplerate, data):
    # Force int16 format before saving
    if data.dtype != np.int16:
        data = data.astype(np.int16)
    wavfile.write(filepath, samplerate, data)

def play_audio(data, samplerate):
    sd.play(data, samplerate)
    sd.wait()

def audio_to_bits(audio_array):
    # Convert int16 array to packed bit array
    audio_bytes = audio_array.astype(np.int16).tobytes()
    return np.unpackbits(np.frombuffer(audio_bytes, dtype=np.uint8))

def bits_to_audio(bits):
    audio_bytes = np.packbits(bits)

    # Ensure even length for int16 conversion
    if len(audio_bytes) % 2 != 0:
        audio_bytes = audio_bytes[:-1]

    return np.frombuffer(audio_bytes, dtype=np.int16)
