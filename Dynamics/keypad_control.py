import socketio
import keyboard
from time import sleep

sio = socketio.Client()

v = 5
t = 3

@sio.event
def connect():
    while True:
        linvel = 0
        angvel = 0
        print('checking keyboard')
        if keyboard.is_pressed('w'):
            linvel += v
        if keyboard.is_pressed('s'):
            linvel -= v
        if keyboard.is_pressed('d'):
            angvel += t
        if keyboard.is_pressed('a'):
            angvel -= t
        if keyboard.is_pressed(' '):
            linvel *= 2
            angvel *= 2
        drive_msg = {'linear_velocity': linvel, 'angular_velocity': angvel,
                     'linear_aceleration': 0, 'angular_aceleration': 0}
        print(drive_msg)
        sio.emit('/drive_cmd', drive_msg)
        sleep(0.01)

sio.connect("http://192.168.4.25:3000")