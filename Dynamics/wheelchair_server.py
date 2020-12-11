import socketio
from wheelchair_controller import WheelchairController
from math import pi
import time

robot = WheelchairController()
sio = socketio.Client()

states = {'roll':0, 'pitch':0, 'left_castor_angle':0, 'right_castor_angle':0,
        'linear_velocity': 0, 'angular_velocity': 0, 'position': [0, 0], 'heading': 0}

wheels = [0, 0]

C_FAC = 0.5

def calculate_velocities():
    lin, ang = robot.calc_speed(wheels[0], wheels[1])
    states['linear_velocity'] = lin
    states['angular_velocity'] = ang

lin_vel = 0.0
ang_vel = 0.0
lin_acel = 0.0
ang_acel = 0.0

@sio.event
def connect():
    sio.emit("subscribe", ["/caster_angle/left", "/caster_angle/right",
    "/wheel_speed/left", "/wheel_speed/right", "/orientation", "/drive_cmd",
    "/trajectory", "/position"])
    print('Connected successfully')

@sio.event
def connect_error():
    print('Failed to connect :(')
@sio.event
def disconnect():
    print('Connection Lost')

@sio.on('/orientation')
def imu(data):
    states['roll']=  data['roll'] * pi/180
    states['pitch'] = data['pitch'] * pi/180

    states['heading'] = data['yaw'] * pi/180

@sio.on('/caster_angle/left')
def caster_left(data):
    states['left_castor_angle'] = data

@sio.on('/caster_angle/right')
def caster_right(data):
    states['right_castor_angle'] = data

@sio.on('/wheel_speed/left')
def left_wheel(data):
    wheels[0] = data
    lin, ang = robot.calc_speed(wheels[0], wheels[1])
    states['linear_velocity'] = lin
    states['angular_velocity'] = ang

@sio.on('/wheel_speed/right')
def right_wheel(data):
    wheels[1] = data
    lin, ang = robot.calc_speed(wheels[0], wheels[1])
    states['linear_velocity'] = lin
    states['angular_velocity'] = ang

@sio.on('/drive_cmd')
def on_drive_cmd(data):
    lin_vel = data['linear_velocity']
    ang_vel = data['angular_velocity']
    lin_acel = data['linear_aceleration']
    ang_acel = data['angular_aceleration']

    calculate_velocities()
    robot.update_states(states)
    #left, right = robot.velocity_control(lin_vel, ang_vel, lin_acel, ang_acel)
    left, right = robot.simplified_velocity_control(lin_vel, ang_vel, lin_acel, ang_acel)
    sio.emit("/set_torques", [left, right])
    #print("Castor L: % .2f, Castor R: % .2f  (deg)| Vel: % .2f (m/s), % .2f (rad/s)|Target Vel: % .2f (m/s), % .2f (rad/s) | Torque: % .2f, % .2f (Nm)"
    #      %(states['left_castor_angle']*180/pi, states['right_castor_angle']*180/pi, states['linear_velocity'], states['angular_velocity'],lin_vel, ang_vel, left, right))
    print("X: % .2f Y: % .2f ANG: %.2f, Lin: % .2f, Ang: % .2f,T1: % .2f, T2: % .2f" %(states['position'][0], states['position'][1], states['heading'],lin_vel, ang_vel, left, right))

@sio.on('/position')
def on_position(data):
    states['position'] = [data['x'] / 100, data['y'] / 100]

@sio.on('/trajectory')
def on_trajectory(data):
    print("Starting path follow")
    print("Length of data: ", len(data))
    print("Starting point: ", data[0])
    print("Down-sample: ", data[::10])
    traj = data
    while not robot.pursuit_is_done(traj, states['position']):
        lin_vel, ang_vel = robot.pursue(traj, states['position'], states['heading'])

        data = {'linear_velocity': lin_vel* C_FAC, "angular_velocity": ang_vel* C_FAC, "linear_aceleration": 0, "angular_aceleration": 0 }
        on_drive_cmd(data)
        time.sleep(0.05)
    print("Reached Target")
sio.connect('http://localhost:3000')
