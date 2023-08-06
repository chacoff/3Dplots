import numpy as np
import scipy.linalg
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd
import pyvista as pv

pv.set_plot_theme("paraview")  # paraview, dark, document

data2plot = pd.read_csv('3D_graph_.csv', delimiter=',', engine='python')

# Data for a three-dimensional line
xline = data2plot['ΔH(mm)'].to_numpy()
xline = xline/10  # quick visualization fix to shrink the length
yline = data2plot['ΔR(deg)'].to_numpy()
zline = data2plot['WP(m)'].to_numpy()
# zline = (1000*zline).astype('int')  # to mm
data = np.array((xline, yline, zline)).T

cloud = pv.PolyData(data)
# cloud.plot(render_points_as_spheres=True)

z_array = data[:, -1]  # Make data array using z-component of points array
cloud["WP(m)"] = z_array  # Add that data to the mesh with the name "uniform dist"

volume = cloud.delaunay_3d(alpha=2500., offset=4, progress_bar=True)
shell = volume.extract_surface(progress_bar=True)  # extract_geometry()
shell.plot(show_bounds=False, window_size=[600, 600], notebook=False)  # eye_dome_lighting=True, render_points_as_spheres=True


'''
X, Y = np.meshgrid(np.arange(0, 220, 20), np.arange(0, 12, 2))
XX = X.flatten()
YY = Y.flatten()

# best-fit linear plane
A = np.c_[np.ones(data.shape[0]), data[:, :2], np.prod(data[:, :2], axis=1), data[:, :2] ** 2]
C, _, _, _ = scipy.linalg.lstsq(A, data[:, 2])
Z = (np.dot(np.c_[np.ones(XX.shape), XX, YY, XX * YY, XX ** 2, YY ** 2], C).reshape(X.shape))

fig = plt.figure()
ax = plt.axes(projection='3d')

# ax.plot3D(xline, yline, zline, 'orange')
ax.scatter3D(xline, yline, zline, c=zline, cmap='Oranges', s=50)
# ax.plot_surface(X, Y, Z, cmap='Oranges', edgecolor='none', rstride=1, cstride=1, alpha=0.6)
plt.xlabel('ΔH(mm)')
plt.ylabel('ΔR(deg)')
ax.set_zlabel('WP(m)')
ax.set_title('Water pressure')
plt.show()
'''