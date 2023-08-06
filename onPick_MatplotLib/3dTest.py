import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')

# Prepare arrays x, y, z
x = np.arange(5)
y = np.arange(5)*4
z = np.arange(5)*100

line, = ax.plot(x, y, z, label='curve')

fig.canvas.draw()

xdata, ydata, zdata = line._verts3d
print(xdata)  # This prints [0 1 2 3 4]

plt.show()