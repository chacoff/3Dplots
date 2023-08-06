from mpl_toolkits.mplot3d import proj3d
import matplotlib.pyplot as plt

import matplotlib

print('matplotlib: {}'.format(matplotlib.__version__))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = [0, 2, 0, 0]
y = [0, 2, 0, 2]
z = [0, 2, 2, 0]

scatter = ax.scatter(x, y, z, picker=True)


def chaos_onclick(event):
    point_index = int(event.ind)
    print(point_index)

    # proj = ax.get_proj()
    # x_p, y_p, _ = proj3d.proj_transform(x[point_index], y[point_index], z[point_index], proj)
    # plt.annotate(str(point_index), xy=(x_p, y_p))

    print("X=", x[point_index], " Y=", y[point_index], " Z=", z[point_index], " PointIdx=", point_index)


fig.canvas.mpl_connect('pick_event', chaos_onclick)
plt.show()