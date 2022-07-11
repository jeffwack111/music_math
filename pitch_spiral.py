import sys
import matplotlib.pyplot as plt
import sounddevice as sd
from matplotlib.patches import Wedge
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSlider
import scipy.signal as sig

class IntervalSpiral(QWidget):
    def __init__(self):
        super().__init__()

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.axes = self.canvas.figure.subplots()

        self.freq_ratio = 1

        self.ratio_input = QSlider(self)
        self.ratio_input.setValue(1000)
        self.ratio_input.setMinimum(1000)
        self.ratio_input.setMaximum(2000)
        self.ratio_input.valueChanged.connect(self.update)

        self.slider_label = QLabel(self)
        self.slider_label.setText(f"frequency ratio = {self.freq_ratio}")

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.ratio_input)
        vlayout.addWidget(self.slider_label)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.canvas)
        hlayout.addLayout(vlayout)

        self.setLayout(hlayout)

        self.th_width = 360/128
        self.max_otone = 64
        self.n_spiral = 10000

        self.plot_spiral_and_root()     

    def plot_spiral_and_root(self):

        th_width = self.th_width
        n_otone = self.max_otone
        n_spiral = self.n_spiral

        x = np.zeros(n_spiral)
        y = np.zeros(n_spiral)

        for p,point in enumerate(np.linspace(1,n_otone*2,n_spiral)):
            theta = np.log(point)*2*np.pi/np.log(2)
            r = 1+theta/(2*np.pi)

            x[p] = r*np.cos(theta)
            y[p] = r*np.sin(theta)

        self.axes.plot(x,y,color = 'black')

        for otone in range(1,n_otone+1):
            theta = np.log(otone)*360/np.log(2)
            r = 1+ theta/360
            self.axes.add_artist(Wedge((0,0),r,theta-th_width,theta+th_width,width = 1,alpha = 1/otone))

    def plot_note(self):
        th_width = self.th_width
        n_otone = self.max_otone
        for otone in range(1,n_otone+1):
            theta = np.log(otone*self.freq_ratio)*360/np.log(2)
            r = 1+ theta/360
            self.axes.add_artist(Wedge((0,0),r,theta-th_width,theta+th_width,width = 1,color='orange',alpha = 1/otone))

    def update(self):
        self.freq_ratio = float(self.ratio_input.value())/1000
        self.slider_label.setText(f"frequency ratio = {self.freq_ratio}")
        self.axes.clear()
        self.plot_spiral_and_root()
        self.plot_note()
        self.canvas.draw()

cycleA = 0
cycleB = 0
root_freq = 200

def callback(outdata, frames, time, status):
    global w
    global cycleA
    global cycleB
    t = (np.arange(frames)) / 44100
    t = t.reshape(-1, 1)
    #print(t)
    outdata[:] += 0.1 * sig.sawtooth(2*np.pi*(root_freq*t+cycleA),width=0.5)
    outdata[:] +=  0.1 * sig.sawtooth(2*np.pi*(root_freq*w.freq_ratio*t+cycleB),width=0.5)
    cycleA = (root_freq*frames/44100+cycleA)%1
    cycleB = (root_freq*w.freq_ratio*frames/44100+cycleB)%1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = IntervalSpiral()
    w.show()
    with sd.OutputStream(device=3, channels=1, callback=callback, samplerate=44100):
        app.exec()

