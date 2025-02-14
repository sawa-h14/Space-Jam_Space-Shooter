import math, random
from panda3d.core import *

def Cloud(radius = 1):
    x = 2 * random.random() - 1
    y = 2 * random.random() - 1
    z = 2 * random.random() - 1
    unitVec = Vec3(x, y, z)
    unitVec.normalize()

    return unitVec * radius

def BaseballSeams(step, numSeams, B, F = 1):
    time = step / float(numSeams) * 2 * math.pi

    F4 = 0

    R = 1

    xxx = math.cos(time) - B * math.cos(3 * time)
    yyy = math.sin(time) + B * math.sin(3 * time)
    zzz = F * math.cos(2 * time) + F4 * math.cos(4 * time)

    rrr = math.sqrt(xxx ** 2 + yyy ** 2 + zzz ** 2)

    x = R * xxx / rrr
    y = R * yyy / rrr
    z = R * zzz / rrr

    return Vec3(x, y, z)

def CircleX(step, numSeams):
    theta = step / float(numSeams) * 2 * math.pi
    x = 0.0 * math.tan(theta), 50.0 * math.cos(theta), 50.0 * math.sin(theta)
    return Vec3(x)

def CircleY(step, numSeams):
    theta = step / float(numSeams) * 2 * math.pi
    y = 50.0 * math.cos(theta), 0.0 * math.tan(theta), 50.0 * math.sin(theta)
    return Vec3(y)

def CircleZ(step, numSeams):
    theta = step / float(numSeams) * 2 * math.pi
    z = 50.0 * math.cos(theta), 50.0 * math.sin(theta), 0.0 * math.tan(theta)
    return Vec3(z)
