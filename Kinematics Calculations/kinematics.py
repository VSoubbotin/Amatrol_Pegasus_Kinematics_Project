import math
import numpy as np
from matplotlib import pyplot

xPt = []
yPt = []
zPt = []
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

def solve(pX, pY, pZ, facing, solution): #converts x y z pos to axis positions
    solA = math.degrees(math.atan2(pX, pY)) #axis 1 angle, "points" at x y position
    if facing != True: solA -= math.copysign(180, solA) #if position "behind" axis 2 turn 180

    lX = math.sqrt(pX ** 2 + pY ** 2) #top down distance between center of axis 1 rotation to x y point
    if facing != True: lX *= -1 #if position solution "behind" axis 2
    lY = pZ #arm plane y position, equal to z position
    r = math.sqrt(lX ** 2 + lY ** 2) #arm plane distance betwen axis 2 and point
    if r > (rA + rB): return #is point out of reach (distance larger then combined arm length)

    n = (r ** 2 + rA ** 2 - rB ** 2) / 2 #term used in quadratic multiple times
    xTerm = (n * lX) / (r ** 2) #-b term of quadratic formula, over 2a for x coordinate
    yTerm = (n * lY) / (r ** 2) #-b term of quadratic formula, over 2a for y cooridnate
    xRoot = math.sqrt((n ** 2 * lX ** 2) - (r ** 2 * (n ** 2 - (lY ** 2 * rA ** 2)))) / (r ** 2) #root b^2-4ac term of quadratic, over 2a for x coordinate
    yRoot = math.sqrt((n ** 2 * lY ** 2) - (r ** 2 * (n ** 2 - (lX ** 2 * rA ** 2)))) / (r ** 2) #root b^2-4ac term of quadratic, over 2a for y coordinate
    
    x1 = xTerm - math.copysign(xRoot, lY) #swaps order of solutions when arm plane y < 0
    x2 = xTerm + math.copysign(xRoot, lY)
    
    y1 = yTerm + math.copysign(yRoot, lX) #swaps order of solutions when arm plane x < 0
    y2 = yTerm - math.copysign(yRoot, lX)
    
    forwardSol = math.degrees(math.atan2(y1, x1))
    inverseSol = math.degrees(math.atan2(y2, x2))
    
    if solution == True:
        solB = forwardSol #angle of axis 2
        solC = inverseSol #angle of axis 3, relative to axis 2. this is useful to ensure that they are not colliding, but the robot takes an absolute input
    else:
        solB = inverseSol
        solC = forwardSol
    return solA, solB, solC

def convert(A, B, C, D, E, *argv): 
    if len(argv) == 0:
        degA = np.clip(A, -170, 170)
        degB = np.clip(B, -15, 140)
        degC = np.clip(C, -135 + degB, 135 + degB)
        degD = np.clip(D, -135 + degC, 135 + degC)
        degE = E % 360 - 180
    elif argv[0] == True:
        degA = A
        degB = B
        degC = C
        degD = D
        degE = E
    aRatio = (2048 * 19.7 * (50 / 2)) / 360 #encoder CPR, gearmotor ratio, chain ratio, per degree
    bRatio = (2048 * 19.7 * (50 / 2)) / 360
    cRatio = (2048 * 65.5 * (32 / 9)) / 360
    dRatio = (2048 * 65.5 * (20 / 9)) / 360
    eRatio = (2048 * 65.5 * (20 / 9)) / 360
    encA = round(degA * aRatio)
    encB = round((degB - 90) * bRatio)
    encC = round(degC * cRatio)
    encD = round(degD * dRatio + degE * eRatio) #differential control of tilt and rotation of gripper
    encE = round(-degD * dRatio + degE * eRatio)
    return encA, encB, encC, encD, encE

def addPoint(x, y, z, A, B, facing, solution):
    solA, solB, solC = solve(x, y, z, facing, solution)
    encA, encB, encC, encD, encE = convert(solA, solB, solC, A, B)
    formatAppend(encA, encB, encC, encD, encE)
    xPt.append(x)
    yPt.append(y)
    zPt.append(z)

def formatAppend(A, B, C, D, E, *argv):
    if len(argv) != 0:
        pos.append(argv[0] + "," + str(A) + "," + str(B) + "," + str(C) + "," + str(D) + "," + str(E))
    else:
        pos.append("Point_" + str(len(pos)) + "," + str(A) + "," + str(B) + "," + str(C) + "," + str(D) + "," + str(E))

def fileGen(name, Fprg, Fenc, Fpts, Fios):
    np.savetxt(name + ".prg", Fprg, fmt='%s')
    np.savetxt(name + ".enc", Fenc, fmt='%s')
    np.savetxt(name + ".pts", Fpts, fmt='%s')
    np.savetxt(name + ".ios", Fios, fmt='%s')

def progGen():
    print('test')

def xyLine(sX, sY, eX, eY, Z, subStep, clearance):
    xStep = (eX - sX) / subStep
    yStep = (eY - sY) / subStep
    addPoint(sX, sY, Z + clearance, -90, math.degrees(math.atan2(sY, sX)) + 90, True, True)
    for i in range(subStep):
        addPoint(sX, sY, Z, -90, math.degrees(math.atan2(sY, sX)) + 90, True, True)
        print(i, sX, sY)
        sX += xStep
        sY += yStep
    addPoint(sX, sY, Z + clearance, -90, math.degrees(math.atan2(sY, sX)) + 90, True, True)

def contLine(eX, eY, Z, subStep, clearance):
    
    xStep = (eX - sX) / subStep
    yStep = (eY - sY) / subStep
    addPoint(sX, sY, Z + clearance, -90, math.degrees(math.atan2(sY, sX)) + 90, True, True)
    for i in range(subStep):
        addPoint(sX, sY, Z, -90, math.degrees(math.atan2(sY, sX)) + 90, True, True)
        print(i, sX, sY)
        sX += xStep
        sY += yStep
    addPoint(sX, sY, Z + clearance, -90, math.degrees(math.atan2(sY, sX)) + 90, True, True)

rA = 9 #axis 2 length
rB = 9 #axis 3 length
pos = []
pos.append("<home>,0,0,0,0,0")
f = 144
deg = math.pi * 2 / 36
r = 1
facing = True
solution = True
xyLine(0, 11, 5, 11, -3, 5, 0)
xyLine(5, 11, 5, 6, -3, 5, 0)
xyLine(5, 6, 0, 6, -3, 5, 0)
xyLine(0, 6, 0, 11, -3, 5, 0)
# for i in range(f):
#     x = r * (i / 72) * math.cos(i * deg)
#     y = 11 + r * (i / 72) * math.sin(i * deg)
#     z = -3
#     xPt.append(x)
#     yPt.append(y)
#     zPt.append(z)
#     if i == 0:
#         solA, solB, solC = solve(x, y, z + 1, facing, solution)
#         encA, encB, encC, encD, encE = convert(solA, solB, solC, -90, math.degrees(math.atan2(y, x)) + 90)
#         formatAppend(encA, encB, encC, encD, encE)
#     solA, solB, solC = solve(x, y, z, facing, solution)
#     encA, encB, encC, encD, encE = convert(solA, solB, solC, -90, math.degrees(math.atan2(y, x)) + 90)
#     formatAppend(encA, encB, encC, encD, encE)


looped = ["""
Accel 255
Linear 255
Speed 255
For i = 1 to """ + str(len(pos) - 1) + """
Tmove pt(i)
Next"""]
sequential = ["""
Accel 255
Linear 255
Speed 255"""]
for i in range(len(pos)): sequential.append('Pmove pt(' + str(i + 1) + ')')

ios = []
for i in range(32): ios.append(("Input_" * (i < 16)) + ("Output_" * (i >= 16)) + str(i % 16 + 1))
pts = ["<home>,0,0,0,0,0"]

fileGen("output15", sequential, pos, pts, ios)

fig = plt.figure()
ax = plt.axes(projection="3d")
fig = plt.plot(xPt, yPt, zPt)
ax.set_xlim3d(-18,18)
ax.set_ylim3d(-18,18)
ax.set_zlim3d(-18,18)
plt.show()