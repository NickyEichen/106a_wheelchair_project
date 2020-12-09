import socketio

sio = socketio.Client()
sio.connect('http://localhost:3000')

d = None

@sio.on('/camera_info')
def on_camera_info(data):
    d = data

@sio.event
def connect():
    sio.emit("subscribe", ["/camera_info"])
    print('Connected successfully')



while True:
    print(d)
    sleep(1)
