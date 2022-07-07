import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5.QtCore import Qt, Slot, Signal
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QSlider
)

class IntervalSpiral(QWidget):
    def __init__(self):
        super().__init__()

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.axes = self.canvas.figure.subplots()

        self.freq_ratio = 1.5

        self.ratio_input = QSlider(Qt.Vertical, self)
        self.ratio_input.setValue(1)
        self.ratio_input.setMinimum(1)
        self.ratio_input.setMaximum(4)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.canvas)
        hlayout.addWidget(self.ratio_input)

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

        for p,point in enumerate(np.linspace(1,n_otone,n_spiral)):
            theta = np.log(point)*2*np.pi/np.log(2)
            r = 1+theta/(2*np.pi)

            x[p] = r*np.cos(theta)
            y[p] = r*np.sin(theta)

        self.axes.plot(x,y,color = 'black')

        for otone in range(1,n_otone+1):
            theta = np.log(otone)*360/np.log(2)
            r = 1+ theta/360
            self.axes.add_artist(Wedge((0,0),r,theta-th_width,theta+th_width,width = 1))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = IntervalSpiral()
    w.show()
    app.exec()

