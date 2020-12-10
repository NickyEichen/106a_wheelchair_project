import socketio

sio = socketio.Client()

d = None

@sio.event
def connect():
    sio.emit("subscribe", ["/caster_angle/left"])
    print('Connected successfully')

@sio.on('/caster_angle/left')
def on_camera_info(data):
    d = data
    print(d)

sio.connect('http://localhost:3000')
