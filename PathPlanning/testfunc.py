def set1():
    x,y,z = -4,1,0
    qx, qy, qz, qw = 1,0,0,0
    transforms = dict(location=[x, y, z], rotation=[qx, qy, qz, qw])
    waypoint = dict(timestamp=0.0, transforms=transforms)
    sio.emit('/path', waypoint)
    # sleep(5)
    x,y,z = -2,-2,0
    qx, qy, qz, qw = 0,0,0,0
    transforms = dict(location=[x, y, z], rotation=[qx, qy, qz, qw])
    waypoint = dict(timestamp=1.0, transforms=transforms)
    sio.emit('/path', waypoint)
    # sleep(5)
    x,y,z = 0,0,0
    qx, qy, qz, qw = 0,0,0,0
    transforms = dict(location=[x, y, z], rotation=[qx, qy, qz, qw])
    waypoint = dict(timestamp=2.0, transforms=transforms)
    sio.emit('/path', waypoint)
    # sleep(5)

def set2():
    x,y,z = -6,-5,0
    qx, qy, qz, qw = 1,0,0,0
    transforms = dict(location=[x, y, z], rotation=[qx, qy, qz, qw])
    waypoint = dict(timestamp=0.0, transforms=transforms)
    sio.emit('/path', waypoint)
    # sleep(5)
    x,y,z = -2,-3,0
    qx, qy, qz, qw = 0,0,0,0
    transforms = dict(location=[x, y, z], rotation=[qx, qy, qz, qw])
    waypoint = dict(timestamp=1.0, transforms=transforms)
    sio.emit('/path', waypoint)
    # sleep(5)
    x,y,z = 0,0,0
    qx, qy, qz, qw = 0,0,0,0
    transforms = dict(location=[x, y, z], rotation=[qx, qy, qz, qw])
    waypoint = dict(timestamp=2.0, transforms=transforms)
    sio.emit('/path', waypoint)
    # sleep(5)
    x,y,z = 2,3,0
    qx, qy, qz, qw = 0,0,0,0
    transforms = dict(location=[x, y, z], rotation=[qx, qy, qz, qw])
    waypoint = dict(timestamp=3.0, transforms=transforms)
    sio.emit('/path', waypoint)
    # sleep(5)

def set3():
    x,y,z = -6,-5,0
    qx, qy, qz, qw = 1,0,0,0
    transforms = dict(location=[x, y, z], rotation=[qx, qy, qz, qw])
    waypoint = dict(timestamp=0.0, transforms=transforms)
    sio.emit('/path', waypoint)
    # sleep(5)
    x,y,z = -2,-3,0
    qx, qy, qz, qw = 0,0,0,0
    transforms = dict(location=[x, y, z], rotation=[qx, qy, qz, qw])
    waypoint = dict(timestamp=1.0, transforms=transforms)
    sio.emit('/path', waypoint)
    # sleep(5)
    x,y,z = 1,2,0
    qx, qy, qz, qw = 0,0,0,0
    transforms = dict(location=[x, y, z], rotation=[qx, qy, qz, qw])
    waypoint = dict(timestamp=2.0, transforms=transforms)
    sio.emit('/path', waypoint)
    # sleep(5)
    x,y,z = 2,3,0
    qx, qy, qz, qw = 0,0,0,0
    transforms = dict(location=[x, y, z], rotation=[qx, qy, qz, qw])
    waypoint = dict(timestamp=3.0, transforms=transforms)
    sio.emit('/path', waypoint)
    # sleep(5)
    x,y,z = 3,8,0
    qx, qy, qz, qw = 0,0,0,0
    transforms = dict(location=[x, y, z], rotation=[qx, qy, qz, qw])
    waypoint = dict(timestamp=4.0, transforms=transforms)
    sio.emit('/path', waypoint)
    # sleep(5)

def set4():
    x,y,z = -2,-1,0
    qx, qy, qz, qw = 1,0,0,0
    transforms = dict(location=[x, y, z], rotation=[qx, qy, qz, qw])
    waypoint = dict(timestamp=0.0, transforms=transforms)
    sio.emit('/path', waypoint)
    # sleep(5)
    x,y,z = 0,-5,0
    qx, qy, qz, qw = 0,0,0,0
    transforms = dict(location=[x, y, z], rotation=[qx, qy, qz, qw])
    waypoint = dict(timestamp=1.0, transforms=transforms)
    sio.emit('/path', waypoint)
    # sleep(5)
    x,y,z = 1,-7,0
    qx, qy, qz, qw = 0,0,0,0
    transforms = dict(location=[x, y, z], rotation=[qx, qy, qz, qw])
    waypoint = dict(timestamp=2.0, transforms=transforms)
    sio.emit('/path', waypoint)
    # sleep(5)



