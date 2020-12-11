import socketio
import keyboard
from time import sleep

sio = socketio.Client()

v = 5
t = -3

exit = False

@sio.event
def connect():
    print("connected successfully")
    exit = False
    while not exit:
        linvel = 0
        angvel = 0
        if keyboard.is_pressed('w'):
            linvel += v
        if keyboard.is_pressed('s'):
            linvel -= v
        if keyboard.is_pressed('d'):
            angvel += t
        if keyboard.is_pressed('a'):
            angvel -= t
        drive_msg = {'linear_velocity': linvel, 'angular_velocity': angvel,
                     'linear_aceleration': 0, 'angular_aceleration': 0}
        sio.emit('/drive_cmd', drive_msg)
        sleep(0.01)

@sio.event
def disconnect():
    print("Disconnected")
    exit = True

sio.connect('http://localhost:3000')
