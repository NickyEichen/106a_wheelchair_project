import pathfinder as pf
import math
import numpy as np

def get_closest(traj, pos):
    ind=0
    d_min=float('Inf')
    for i, pt in enumerate(reversed(traj)):
        dist = math.sqrt((pt[0]-pos[0])**2 + (pt[1]-pos[1])**2)
        if dist < d_min:
            ind = i
            d_min = dist
    return len(traj) - ind - 1

def lookahead(traj, pos, r):
    if math.sqrt(traj[-1][0]**2 + traj[-1][1]**2) < r:
        x, y = traj[-1][0], traj[-1][1]
        t_ind = len(traj) - 1
        return x, y, t_ind

    x, y = 0, 0
    t_ind = 0
    for i, pt in enumerate(reversed(traj[:-1])):
        j = len(traj) - 2 - i
        d = (traj[j+1][0] - pos[0], traj[j][1] - pos[1])
        f = (pt[0] - pos[0], pt[1] - pos[1])

        a = sum(x**2 for x in d)
        b = 2*sum(x * y for x, y in zip(d, f))
        c = sum(y**2 - r**2 for y in f)

        disc = b**2 - 4*a*c
        if disc >= 0:
            disc = math.sqrt(disc)
            t1 = (-b - disc) / (2*a)
            t2 = (-b + disc) / (2*a)

            if (t1 >= 0 and t1 <= 1):
                x, y = pt[0] + t1*d[0], pt[1] + t1*d[1]
                t_ind = j
                return x, y, t_ind
            if (t2 >= 0 and t2 <= 1):
                x, y = pt[0] + t2*d[0], pt[1] + t2*d[1]
                t_ind = j
                return x, y, t_ind

    ind = get_closest(traj, pos)
    x, y = traj[ind][0], traj[ind][1]
    return x, y, t_ind

def curvature(traj, pos, x, y, ang):
    ## Calculate curvature math
    side = np.sign(math.sin(math.pi/2 - ang)*(x-pos[0]) - math.cos(math.pi/2 - ang)*(y-pos[1]))
    a = -math.tan(math.pi/2 - ang)
    c = math.tan(math.pi/2 - ang)*pos[0] - pos[1]
    x = abs(a*x + y + c) / math.sqrt(a**2 + 1)
    return side * x / 20

def find_vels(traj, pos, ang, lookahead_dist):
    cst = get_closest(traj, pos)
    x, y, t_ind = lookahead(traj, pos, lookahead_dist)
    c = curvature(traj, pos, x, y, ang)
    vel, ang = traj[cst][2], traj[cst][2] * c
    return vel, ang

def bang_bang(traj, pos, ang, coef):
    cst = get_closest(traj, pos)
    x, y, t_ind = lookahead(traj, pos, 0.6)

    v_x, v_y = x - pos[0], y - pos[1]
    e_ang = math.atan2(v_y, v_x) - ang
    return traj[cst][2], e_ang * coef


def is_done(traj, pos, done_dist):
    print(traj[-1], pos)
    print("Dist:", (traj[-1][0] - pos[0])**2 + (traj[-1][1] - pos[1])**2)
    if (traj[-1][0] - pos[0])**2 + (traj[-1][1] - pos[1])**2 < done_dist**2 or get_closest(traj, pos) >= len(traj) - 10:
        print("DONE")
        return True
    return False
