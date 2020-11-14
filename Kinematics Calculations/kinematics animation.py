import math
import numpy as np
from matplotlib import pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

def solve(pX, pY, pZ, facing, solution): #converts x y z pos to axis positions
    solA = math.atan2(pX, pY) #axis 1 angle, "points" at x y position
    if facing != True: solA -= math.copysign(math.pi, solA) #if position "behind" axis 2 turn 180

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
    
    forwardSol = math.atan2(y1, x1)
    inverseSol = math.atan2(y2, x2)
    
    if solution == True:
        solB = forwardSol #angle of axis 2
        solC = inverseSol #angle of axis 3, relative to axis 2. this is useful to ensure that they are not colliding, but the robot takes an absolute input
    else:
        solB = inverseSol
        solC = forwardSol
    return solA, solB, solC

def appendArm(A, B, C):
    gX.append(0)
    gY.append(0)
    gZ.append(0)
    gX.append(rA * math.sin((math.pi / 2) - B) * math.cos(A))
    gY.append(rA * math.sin((math.pi / 2) - B) * math.sin(A))
    gZ.append(rA * math.cos((math.pi / 2) - B))
    gX.append(gX[len(gX) - 1] + rB * math.sin((math.pi / 2) - C) * math.cos(A))
    gY.append(gY[len(gY) - 1] + rB * math.sin((math.pi / 2) - C) * math.sin(A))
    gZ.append(gZ[len(gZ) - 1] + rB * math.cos((math.pi / 2) - C))

def appendPt(A, B, C):
    gX.append(rA * math.sin((math.pi / 2) - B) * math.cos(A) + rB * math.sin((math.pi / 2) - C) * math.cos(A))
    gY.append(rA * math.sin((math.pi / 2) - B) * math.sin(A) + rB * math.sin((math.pi / 2) - C) * math.sin(A))
    gZ.append(rA * math.cos((math.pi / 2) - B) + rB * math.cos((math.pi / 2) - C))

rA = 9
rB = 9
aSpeed = 160 * (2 / 50) * 2 * math.pi
bSpeed = 160 * (2 / 50) * 2 * math.pi
cSpeed = 160 * (9 / 32) * 2 * math.pi
dSpeed = 160 * (9 / 20) * 2 * math.pi
eSpeed = 160 * (9 / 20) * 2 * math.pi

gX = []
gY = []
gZ = []

sX = 0
sY = 8
sZ = 6

subStep = 15
proportional = False
facing = True
solution = True

eX = 8
eY = 12
eZ = -3

sA, sB, sC = solve(sX, sY, sZ, facing, solution)
eA, eB, eC = solve(eX, eY, eZ, facing, solution)
appendArm(eA, eB, eC)
appendArm(sA, sB, sC)
dA = eA - sA
dB = eB - sB
dC = eC - sC
t = max(abs(dA) / aSpeed, abs(dB) / bSpeed, abs(dC) / cSpeed)
dt = t / subStep
if proportional == False:
    aStep = math.copysign(aSpeed * dt, dA)
    bStep = math.copysign(bSpeed * dt, dB)
    cStep = math.copysign(cSpeed * dt, dC)
else:
    aStep = dA / subStep
    bStep = dB / subStep
    cStep = dC / subStep
iA = sA
iB = sB
iC = sC
for i in range(subStep):
    if abs(dA) >= abs(aStep):
        dA = math.copysign(abs(dA) - abs(aStep), dA)
        iA += aStep
    elif dA != 0:
        iA += dA
        dA = 0
    if abs(dB) >= abs(bStep):
        dB = math.copysign(abs(dB) - abs(bStep), dB)
        iB += bStep
    elif dB != 0:
        iB += dB
        dB = 0
    if abs(dC) >= abs(cStep):
        dC = math.copysign(abs(dC) - abs(cStep), dC)
        iC += cStep
    elif dC != 0:
        iC += dC
        dC = 0
    appendPt(iA, iB, iC)

fig = plt.figure()
ax = plt.axes(projection="3d")
fig = plt.plot(gX, gY, gZ)
ax.set_xlim3d(-18,18)
ax.set_ylim3d(-18,18)
ax.set_zlim3d(-18,18)
#print(gX)
#print(gY)
#print(gZ)
plt.show()


