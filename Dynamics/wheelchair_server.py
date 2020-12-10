import socketio
from wheelchair_controller import WheelchairController

robot = WheelchairController()
sio = socketio.Client()

states = {'roll':0, 'pitch':0, 'left_castor_angle':0, 'right_castor_angle':0,
        'linear_velocity': 0, 'angular_velocity': 0}

left_wheel_speed = 0.0
right_wheel_speed = 0.0
def calculate_velocities():
    lin, ang = robot.calc_speed(left_wheel_speed, right_wheel_speed)
    states['linear_velocity'] = lin
    states['angular_velocity'] = ang

lin_vel = 0.0
ang_vel = 0.0
lin_acel = 0.0
ang_acel = 0.0

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


@sio.on('/drive_cmd')
def on_drive_cmd(data):
    lin_vel = data['linear_velocity']
    ang_vel = data['angular_velocity']
    lin_acel = data['linear_aceleration']
    ang_acel = data['angular_aceleration']

    calculate_velocities()
    robot.update_states(states)
    left, right = robot.velocity_control(lin_vel, ang_vel, lin_acel, ang_acel)
    sio.emit('/set_torques', list([left, right]))
    print("States:", states, " Torques: %.2f, %.2f" %(left, right))

sio.connect('http://localhost:3000')
