import socketio
from wheelchair_controller import WheelchairController
from math import pi

robot = WheelchairController()
sio = socketio.Client()

states = {'roll':0, 'pitch':0, 'left_castor_angle':0, 'right_castor_angle':0,
        'linear_velocity': 0, 'angular_velocity': 0}

wheels = [0, 0]

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
    states['roll']=  data['roll'] * pi/180
    states['pitch'] = data['yaw'] * pi/180

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
    left, right = robot.velocity_control(lin_vel, ang_vel, lin_acel, ang_acel)
    sio.emit("/set_torques", [left, right])
    print("Castor L: % .2f, Castor R: % .2f  (deg)| Vel: % .2f, % .2f | wheel vels: % .2f, % .2f m/s| Torque: % .2f, % .2f (Nm)"
    %(states['left_castor_angle']*180/pi, states['right_castor_angle']*180/pi, states['linear_velocity'], states['angular_velocity'], wheels[0], wheels[1], left, right))

sio.connect('http://localhost:3000')
