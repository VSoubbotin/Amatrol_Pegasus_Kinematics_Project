import math
import numpy as np
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import sys

rA = 9
rB = 9
rT = 6
aRatio = (2048 * 19.7 * (50 / 2)) / (2 * math.pi)#encoder CPR, gearmotor ratio, chain ratio, per rotation
bRatio = (2048 * 19.7 * (50 / 2)) / (2 * math.pi)
cRatio = (2048 * 65.5 * (32 / 9)) / (2 * math.pi)
dRatio = (2048 * 65.5 * (20 / 9)) / (2 * math.pi)
eRatio = (2048 * 65.5 * (20 / 9)) / (2 * math.pi)
mode = "xyzAB"
mode = "abcde"
x = []
y = []
z = []
pitch = []
roll = []
animation = False
showArm = False
data = []
inputFile = open(str(sys.path[0]) + "\posLog.txt")
for i in inputFile: data.append(i)
for i in range(len(data)):
    pt = []
    pt = (data[i]).split(" ")
    t = len(pt) - 1
    for n in range(t):
        if pt[t - n] == '' or pt[t - n] == '\n': del pt[t - n]
    for n in range(len(pt)): pt[n] = float(pt[n])
    if mode == "xyzAB":
        x.append(pt[0])
        y.append(pt[1])
        z.append(pt[2])
        pitch.append(pt[3])
        roll.append(pt[4])
    elif mode == "abcde":
        A = pt[0] / aRatio
        B = pt[1] / bRatio
        C = pt[2] / cRatio
        D = pt[3] / dRatio
        E = pt[4] / eRatio
        tilt = (pt[3] - pt[4]) / (dRatio + eRatio)
        rot = (pt[3] + pt[4]) / (dRatio + eRatio)
        print(tilt)
        print(pt)
        magnitude = rA * math.sin(-B) + rB * math.cos(C) + rT * math.cos(tilt)
        x.append(magnitude * math.cos(A))
        y.append(magnitude * math.sin(A))
        z.append(rA * math.cos(-B) + rB * math.sin(C) + rT * math.sin(tilt))
        pitch.append(tilt)
        roll.append(rot)
fig = plt.figure()
ax = plt.axes(projection="3d")
fig = plt.plot(x, y, z)
ax.set_xlim3d(-18,18)
ax.set_ylim3d(-18,18)
ax.set_zlim3d(-18,18)
plt.show()




    
