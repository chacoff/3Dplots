from functools import lru_cache, wraps

import pandas as pd
from plyfile import PlyData, PlyElement
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import art3d as get3D
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import random
import numpy as np
import hashlib
import seaborn as sns
import os
sns.set(style="darkgrid")


def onpick(event):
    point_index = event.ind

    ix = int(point_index[0])  # we just pick the first one in case there are too many in the same cluster
    print(f'X={x_NonZero[ix]}, Y={y_NonZero[ix]}, Z={z_NonZero[ix]}, PointIdx={ix}')
    line = (float(x_NonZero[ix]), float(y_NonZero[ix]), float(z_NonZero[ix]))

    with open("test.txt", "a") as f:
        f.write("\n")
        np.savetxt(f, line, delimiter=' ', fmt='% s', newline=' ')


def array_cache(function):
    cache = {}

    @wraps(function)
    def wrapped(array):
        # Not using built-in hash because it's prone to collisions.
        return cache.get(hashlib.md5(array.data.tobytes()).digest(), function(array))

    return wrapped


@array_cache
def NonZeroAxis(axis):
    nt = 2
    step1 = axis[axis != 0.0][::nt]
    return step1  # delete all zero elements and every subsampling nt


def main(source):
    # read the ply file
    os.remove('test.txt') if os.path.exists('test.txt') else None
    plydata = PlyData.read(source)
    print(dir(PlyData))
    x = (plydata['vertex']['x'])
    y = (plydata['vertex']['y'])
    z = (plydata['vertex']['z'])

    print(f'{plydata.elements[0].name}: {len(x)} points per axis')

    return [x, y, z]


if __name__ == "__main__":

    data = main(source='ROI-1.ply')

    x_NonZero = NonZeroAxis(data[0])
    y_NonZero = NonZeroAxis(data[1])
    z_NonZero = NonZeroAxis(data[2])

    print(f'non-zero points left: (x, y, z) =  ({len(x_NonZero)}, {len(y_NonZero)}, {len(z_NonZero)})')

    dict_nonZero = {
        'X': x_NonZero,
        'Y': y_NonZero,
        'Z': z_NonZero
    }

    df_nonZero = pd.DataFrame.from_dict(dict_nonZero)
    df_clean = df_nonZero.loc[df_nonZero['Z'] <= 1015]

    mask = df_clean.Z > np.mean(df_clean.Z)
    # pcd = np.column_stack((df_clean.X, df_clean.Y, df_clean.Z))
    # spatial_query = pcd[df_clean.Z > np.mean(df_clean.Z)]

    XY_stack = np.column_stack((df_clean.X[mask], df_clean.Y[mask]))
    kmeans = KMeans(n_clusters=15).fit(XY_stack)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # ax.scatter(df_clean.X, df_clean.Y, df_clean.Z, picker=True, cmap=cm.Paired, s=0.1)
    # ax.scatter(df_clean.X[mask], df_clean.Y[mask], picker=True, cmap=cm.Paired, s=0.1)

    ax.scatter(df_clean.X[mask], df_clean.Y[mask], c=kmeans.labels_, s=0.1, picker=True)

    fig.canvas.mpl_connect('pick_event', onpick)

    plt.axis('on')
    plt.show()
