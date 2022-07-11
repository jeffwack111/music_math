from mimetypes import init
import numpy as np
import sounddevice as sd
import scipy.signal as sig

samplerate = 44100
Bank = []

class Generator():
    def __init__(self,inital_freq):
        self.freq = inital_freq
        self.phase = 0

    def signal(self,t):
        new_phase = ((self.freq*t[-1]+self.phase)%1)
        chunk = 0.5 * np.sin(2 * np.pi * (self.freq * t + self.phase))
        self.phase = new_phase
        return chunk

    def modsignal(self,t,mod):
        new_phase = ((self.freq*t[-1] + self.phase +mod[-1]/(2*np.pi))%1) 
        chunk = 0.2 * np.sin( 2 * np.pi * (self.freq * t + self.phase)+mod)
        self.phase = new_phase
        return chunk

def callback(outdata, frames, time, status):
    global A
    global B
    t = (np.arange(frames)) / samplerate
    t = t.reshape(-1, 1)
    outdata[:] = np.zeros(np.shape(t))
    outdata[:] += A.modsignal(t,B.modsignal(t,C.signal(t)))

A = Generator(440)
B = Generator(330)
C = Generator(220)

with sd.OutputStream(device=3, channels=1, callback=callback, samplerate=samplerate):
    print('#' * 80)
    print('press Return to quit')
    print('#' * 80)
    input()