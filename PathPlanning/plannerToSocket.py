import socketio
from pathFunc import *
from time import sleep
from testfunc import *

sio = socketio.Client()

@sio.event
def connect():
    set1()
    # set2()
    # set3()
    # set4()
    print('Connected successfully')


#taking in waypoints from /waypoints topic, then creating pts -> trajectory -> right and left individual trajectories
@sio.on('/waypoints') 
def pathPlan(data):
    pts = createPoints(new_data)
    info, trajectory = path(pts)
    right, left = rightLeft(trajectory)
    parse = []
    for seg in trajectory:
        parse.append([seg.x, seg.y, seg.velocity])
    #right/left list of these <Segment dt=0.050000 x=-4.174969 y=-1.178583 position=0.002500 velocity=0.100000 acceleration=2.000000 jerk=40.000000 heading=5.498103>
    #this is how right and left look, large list of these

    sio.emit('/trajectory', parse)


sio.connect('http://localhost:3000')
