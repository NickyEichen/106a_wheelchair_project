import socketio
from pathFunc import *

sio = socketio.Client()

states = {'roll':0, 'pitch':0, 'left_castor_angle':0, 'right_castor_angle':0,
        'linear_velocity': 0, 'angular_velocity': 0}


@sio.event
def connect():
    sio.emit("subscribe", ["/caster_angle/left", "/castor_angle/right",
    "/wheel_speed/left", "/wheel_speed/right", "/orientation", "/drive_cmd"])
    print('Connected successfully')

@sio.event
def connect_error():
    print('Failed to connect :(')
@sio.event
def disconnect():
    print('Connection Lost')

@sio.on('/orientation')
def imu(data):
    states['roll']=  data['roll']
    states['pitch'] = data['yaw']

@sio.on('/caster_angle/left')
def caster_left(data):
    states['left_castor_angle'] = data['yaw']

@sio.on('/caster_angle/right')
def caster_right(data):
    states['right_castor_angle'] = data['yaw']

@sio.on('/wheel_speed/left')
def left_wheel(data):
    left_wheel_speed = data

@sio.on('/wheel_speed/right')
def right_wheel(data):
    right_wheel_speed = data


#need to figure out how to recieve waypoints, computer vision aspect and how we comunicate those inputs on socket.io

@sio.on('/drive_cmd') #is this supposed to be an event? Maybe we can call this function when computer vision is done
def pathPlan(data):
    #insert data reorganization here for functions
    new_data = ...
    mx_vel = ...
    mx_accel = ...
    mx_jerk = ...
    dt =  0.05
    widthWheels = ...
    pts = createPoints(new_data)
    info, trajectory = path(pts, mx_vel, mx_accel, mx_jerk, dt)
    right, left = rightLeft(trajectory, widthWheels)
    #need to figure out where to put this or emit to, probably should go to controller, right
    #right/left list of these <Segment dt=0.050000 x=-4.174969 y=-1.178583 position=0.002500 velocity=0.100000 acceleration=2.000000 jerk=40.000000 heading=5.498103>
    #this is how right and left look, large list of these
    sio.emit('/trajectory', trajectory)

@sio.event
def setWay(waypoints):
    sio.emit('/path', waypoints)
sio.connect('http://localhost:3000')
