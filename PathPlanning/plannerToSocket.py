import socketio
from pathFunc import *

sio = socketio.Client()

@sio.event
def connect():
    x,y,z = 0,0,0
    qx, qy, qz, qw = 0,0,0,0

    for i in range(100):
        transforms = dict(location=[x, 0.01, z], rotation=[qx, qy, qz, qw])
        waypoint = dict(timestamp=2.0, transforms=transforms)
        sio.emit("/path", waypoint)
    for i in range(100):
        transforms = dict(location=[0.01, y+1, z], rotation=[qx, qy, qz, qw])
        waypoint = dict(timestamp=2.0, transforms=transforms)
        sio.emit("/path", waypoint)

    
    print('Connected successfully')

# @sio.event
# def connect_error():
#     print('Failed to connect :(')
# @sio.event
# def disconnect():
#     print('Connection Lost')

# #need to figure out how to recieve waypoints, computer vision aspect and how we comunicate those inputs on socket.io

# @sio.on('/waypoints') #is this supposed to be an event? Maybe we can call this function when computer vision is done
# def pathPlan(data):
#     #insert data reorganization here for functions
#     # new_data = ...
#     # mx_vel = ...
#     # mx_accel = ...
#     # mx_jerk = ...
#     # dt =  0.05
#     # widthWheels = ...
#     pts = createPoints(new_data)
#     info, trajectory = path(pts)
#     right, left = rightLeft(trajectory, widthWheels)
#     #need to figure out where to put this or emit to, probably should go to controller, right
#     #right/left list of these <Segment dt=0.050000 x=-4.174969 y=-1.178583 position=0.002500 velocity=0.100000 acceleration=2.000000 jerk=40.000000 heading=5.498103>
#     #this is how right and left look, large list of these
#     sio.emit('/path', trajectory)

# @sio.event
# def setWay(waypoints):
#     sio.emit('/path', waypoints)

sio.connect('http://localhost:3000')
