import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
c=np.array([1,2,3,4])
fig = plt.figure()
fig.set_dpi(100)  #fenstergröße
fig.set_size_inches(7.5, 7.5) #fenster format

ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
m1 = plt.Circle((1, 0), 0.1, fc='blue')
def init():
    m1.center = (1, 0)
    ax.add_patch(m1)
    return m1,


def animate(i):
    x, y =m1.center
    x = i/10
    y = c[i]
    m1.center = (x, y)
    return m1,



anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=100, 
                               interval=1000, #geschwindigkeit
                               blit=True)