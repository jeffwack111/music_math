import numpy as np
import sounddevice as sd
import scipy.signal as sig

samplerate = 44100
start_idx = 0

def callback(outdata, frames, time, status):
    global start_idx
    t = (start_idx + np.arange(frames)) / samplerate
    t = t.reshape(-1, 1)
    outdata[:] = 0.2 * sig.sawtooth(2 * np.pi * 300 * t) + 0.2 * sig.square(2 * np.pi * 200 * t)
    start_idx += frames

with sd.OutputStream(device=3, channels=1, callback=callback, samplerate=samplerate):
    print('#' * 80)
    print('press Return to quit')
    print('#' * 80)
    input()