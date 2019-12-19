import matplotlib
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


fig = plt.figure()
ax = plt.axes(projection='3d')

xpoints = np.linspace(-10, 10, 100)
ypoints = np.linspace(-10, 10, 100)
zpoints = np.zeros( (1, (len(xpoints)* len(ypoints))) )
print(zpoints)
i = 0
for x in xpoints:
    for y in ypoints:
        z = math.sin(x*y)
        zpoints[0][i] += z
#        zpoints.append(z)
print(zpoints)
#print(zpoints)
#Axes3D.plot_surface()
ax.plot_surface(xpoints, ypoints, zpoints)
