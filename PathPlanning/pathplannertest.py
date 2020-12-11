# import sys
# sys.path = ['/Library/Frameworks/Python.framework/Versions/3.9/lib/python39.zip', '/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9', '/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/lib-dynload', '/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages', '/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/pathfinder/_pathfinder.cpython-39-darwin.so']
import pathfinder as pf
import math
import numpy as np
from pathFunc import *

#change these points and run file
points = [
    pf.Waypoint(-2.8, 0.1, 0),   # Waypoint @ x=-4, y=-1, exit angle=-45 degrees
    pf.Waypoint(-1.75, 0.1, 0),
    pf.Waypoint(5, -1.75, math.pi/2), # Waypoint @ x=0, y=0,   exit angle=0 radians
]
# # points = [pf.Waypoint(-4, -1, math.radians(-45.0)), pf.Waypoint(-2, -2, 0), pf.Waypoint(0, 0, 0),]
# info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH, dt=0.05,max_velocity=1.7,max_acceleration=2.0,max_jerk=60.0)


# modifier = pf.modifiers.TankModifier(trajectory).modify(0.5) #0.5 is the width of the wheelchair base need to change
# right = modifier.getRightTrajectory()
# left = modifier.getLeftTrajectory()

# for i in np.arange(len(right)):
#     print(right[i])

info, trajectory = path(points)
print(points, trajectory)

import socketio

sio = socketio.Client()
@sio.event
def connect():
    print("Starting Path")
    data = [list([pt.x, pt.y, pt.velocity]) for pt in trajectory]
    sio.emit("/trajectory", data)
    print("Length of data is:", len(data))
    print("Downsample: ", data[::10])


print("Connecting...")
sio.connect("http://192.168.4.25:3000")