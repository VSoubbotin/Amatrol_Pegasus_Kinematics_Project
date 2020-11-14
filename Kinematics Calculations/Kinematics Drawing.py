import math
import numpy as np
from matplotlib import pyplot
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import sys

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
data = []

xCorner = -4
yCorner = 8
drawZ = -3
scale = 30
clearance = 0.5
curveRes = 0.00001
lineRes = 0.00001
jump = []
xD = []
yD = []
xP = []
yP = []
loop = 0
inputFile = open(str(sys.path[0]) + "\positions.txt")
for i in inputFile: data.append(i)
for i in range(math.floor(len(data))):
    if data[i] == "end\n":
        jump.append(loop)
    else:
        pt = []
        pt = (data[i]).split(" ")
        print((float(pt[0]) / scale + xCorner), (float(pt[1]) / scale + yCorner))
        xD.append(float(pt[0]))
        yD.append(float(pt[1]))
        loop += 1

baseX = min(xD)
baseY = min(yD)

for i in range(loop):
    xD[i] = ((xD[i] - baseX) / scale) + xCorner
    yD[i] = ((yD[i] - baseY) / scale) + yCorner

for i in range(loop):
    print(i)
    print(jump)
    print(xD[i], yD[i])
    jStart = 0
    if i in jump:
        addPoint(xD[i], yD[i], drawZ + clearance, -90, math.degrees(math.atan2(yD[i], xD[i])) + 90, True, True)
        dist = 0
        ang = 0
        jStart = 1
    jEnd = 0
    if i + 1 in jump: jEnd = 1
    if i != 0: 
        prevAng = math.degrees(math.atan2((yD[i] - yD[i - 1]), (xD[i] - xD[i - 1])))
        prevDist = ((yD[i] - yD[i - 1]) ** 2 + (xD[i] - xD[i - 1]) ** 2) ** 0.5
    if i + 1 != loop:
        nextAng = math.degrees(math.atan2((yD[i + 1] - yD[i]), (xD[i + 1] - xD[i])))
        nextDist = ((yD[i + 1] - yD[i]) ** 2 + (xD[i + 1] - xD[i]) ** 2) ** 0.5
    if i != 0:
        if (abs(prevAng + nextAng - prevAng) > curveRes) and ((prevDist and nextDist) + dist > lineRes) or (jStart == 0 and jEnd == 0):
            addPoint(xD[i], yD[i], drawZ, -90, math.degrees(math.atan2(yD[i], xD[i])) + 90, True, True)
            dist = 0
            ang = 0
        else:
            dist += prevDist
            ang += prevAng
    else:
        addPoint(xD[i], yD[i], drawZ, -90, math.degrees(math.atan2(yD[i], xD[i])) + 90, True, True)
        dist = 0
        ang = 0
        xP.append(xD[i])
        yP.append(yD[i])

    if jEnd == 1:
        addPoint(xD[i], yD[i], drawZ + clearance, -90, math.degrees(math.atan2(yD[i], xD[i])) + 90, True, True)



looped = ["""
Accel 32
Speed 128
For i = 1 to """ + str(len(pos) - 1) + """
Tmove pt(i)
Next"""]
sequential = ["""
Accel 32
Speed 128"""]
for i in range(len(pos)): sequential.append('Pmove pt(' + str(i + 1) + ')')

ios = []
for i in range(32): ios.append(("Input_" * (i < 16)) + ("Output_" * (i >= 16)) + str(i % 16 + 1))
pts = ["<home>,0,0,0,0,0"]

fileGen("output22", sequential, pos, pts, ios)

fig = plt.figure()
ax = plt.axes(projection="3d")
fig = plt.plot(xPt, yPt, zPt)
ax.set_xlim3d(-18,18)
ax.set_ylim3d(-18,18)
ax.set_zlim3d(-18,18)
plt.show()

