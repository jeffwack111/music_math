from turtle import width
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np

fig, ax = plt.subplots()
r_width = 1
th_width = 360/128

max_otone = 64
n_spiral = 10000

x = np.zeros(n_spiral)
y = np.zeros(n_spiral)

for p,point in enumerate(np.linspace(1,max_otone,n_spiral)):
    theta = np.log(point)*2*np.pi/np.log(2)
    r = 1+theta*r_width/(2*np.pi)

    x[p] = r*np.cos(theta)
    y[p] = r*np.sin(theta)

ax.plot(x,y,color = 'black')

for otone in range(1,max_otone+1):
    theta = np.log(otone)*360/np.log(2)
    r = 1+ theta*r_width/360
    ax.add_artist(Wedge((0,0),r,theta-th_width,theta+th_width,width = r_width))

r = 10
ax.set_xlim([-r,r])
ax.set_ylim([-r,r])
plt.axis('off')
plt.show()

