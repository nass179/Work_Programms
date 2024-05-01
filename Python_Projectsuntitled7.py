import matplotlib.pyplot as plt

plt.axes()

circle = plt.Circle((0, 0), radius=0.75, fc='y')
plt.gca().add_patch(circle)

plt.axis('scaled')
plt.show()
ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
fig = plt.figure()
fig.set_dpi(100)  #fenstergröße
fig.set_size_inches(7.5, 7.5) #fenster format

ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
m1 = plt.Circle((1, 0), 0.1, fc='blue')
plt.gca().add_patch(circle)