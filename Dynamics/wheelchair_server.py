import socketio
from wheelchair_controller import WheelchairController

robot = WheelchairController()
sio = socketio.Client()

states = {'roll':0, 'pitch':0, 'left_castor_angle':0, 'right_castor_angle':0
        'linear_velocity': 0, 'angular_velocity': 0}

lin_vel = 0.0
ang_vel = 0.0
lin_acel = 0.0
ang_acel = 0.0

@sio.event
def connect():
    print('Connected successfully')
@sio.event
def connect_error():
    print('Failed to connect :(')
@sio.event
def disconnect():
    print('Connection Lost')

@sio.on('/roll')
def on_roll(data):
    states['roll'] = data
# Continue as Necessary

@sio.on('/drive_cmd')
def on_drive_cmd(data):
    lin_vel = data['linear_velocity']
    ang_vel = data['angular_velocity']
    lin_acel = data['linear_aceleration']
    ang_acel = data['angular_velocity']

sio.connect('http://localhost:3000')

while (sio.):
    robot.update_states(states)
    left, right = robot.velocity_control(lin_vel, ang_vel, linear_acel, ang_acel)
    sio.emit('/set_torque', {'left': left, 'right': right})

    sleep(0.05)
