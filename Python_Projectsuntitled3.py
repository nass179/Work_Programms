import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.animation import PillowWriter

plt.style.use('dark_background')

n_points = 100
theta = np.linspace(0, 2 * np.pi, n_points)
e_radius = 5
m_radius = 7

x = e_radius * np.sin(theta)
y = e_radius * np.cos(theta)

xx = m_radius * np.sin(theta)
yy = m_radius * np.cos(theta)

fig, ax = plt.subplots(figsize=(5, 5))
ax = plt.axes(xlim=(-8, 8), ylim=(-8, 8))
earth, = ax.plot([], [], 'g.', markersize=15)
mars, = ax.plot([], [], 'r.', markersize=15)
ax.plot(0, 0, 'X', markersize=5, color="yellow")
plt.grid(True, lw=0.3)
ax.plot(x, y, 'g-')
ax.plot(xx, yy, 'r-')

def animate(i):
    earth.set_data(x[i], y[i])
    mars.set_data(xx[i], yy[i])
    return earth,mars

anim = FuncAnimation(fig, animate, frames=100, interval=200, repeat=False)
#anim.save('cirlce_ani.gif', writer='pillow')
plt.show()