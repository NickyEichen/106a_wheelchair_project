import socketio
from time import sleep

sio = socketio.Client()

v = 5
t = 3

@sio.event
def connect():
    while True:
        s = input("torques >>")
        s1, s2 = s.split(' ')
        t1 = float(s1)
        t2 = float(s2)
        if type(t1) == type (t2) == type(1.2):
            sio.emit('/set_torques', [t1, t2])
        else:
            print("Could not interpret")
        sleep(0.01)

sio.connect('http://192.168.4.25:3000')
