import pathfinder as pf
import math
import numpy as np
import matplotlib.pyplot as plt

"The path planner default trajectory finder is a hermite polynomial function"
# point will be given as [x,y, exit angle]
# so points will be [[x,y, exit angle],[x,y, exit angle],[x,y, exit angle]] etc.
# need to install pip3 install 'pybind11>=2.2'
# pip3 install robotpy-pathfinder
# pip 3install -U matplotlib


def createPoints(points):
    list = []
    for p in points:
        list.append(pf.Waypoint(p[0], p[1], p[2]))
    return list


def path(points, max_vel = 1.7, max_accel = 2.0, max_jerk = 60.0, dt = 0.05):
    info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH, dt, max_vel,max_accel,max_jerk)
    return info, trajectory


"right/left list of these <Segment dt=0.050000 x=-4.174969 y=-1.178583 position=0.002500 velocity=0.100000 acceleration=2.000000 jerk=40.000000 heading=5.498103>"
#can access by right[0].dt = 0.05
def rightLeft(trajectory, widthWheels = 0.5):
    mod = pf.modifiers.TankModifier(trajectory).modify(widthWheels)
    right = modifier.getRightTrajectory()
    left = modifier.getLeftTrajectory()
    return right, left

#plot trajectory through waypoints
def plot(points, trajectory):
    # plot the waypoints
    mx, my = zip(*[(m.y, m.x) for m in points])
    plt.scatter(mx, my, c="r")

    # plot the trajectory
    x, y = zip(*[(seg.y, seg.x) for seg in trajectory])
    plt.plot(x, y)

    plt.xlabel('x variable')
    plt.ylabel('y variable')
    plt.title('Plot of Path Planning Algorithm')
    plt.show()