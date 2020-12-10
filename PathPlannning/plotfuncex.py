import pathfinder as pf
import math

import matplotlib.pyplot as plt

if __name__ == "__main__":

    points = [
        pf.Waypoint(0, 0, 0),
        pf.Waypoint(-10, -1,0),
        pf.Waypoint(-20, -2, 0),
        pf.Waypoint(-50, -3, 0),
    # , math.radians(-45.0))
    ]

    dt = 0.05  # 50ms

    info, trajectory = pf.generate(
        points,
        pf.FIT_HERMITE_CUBIC,
        pf.SAMPLES_HIGH,
        dt=dt,
        max_velocity=1.7,
        max_acceleration=2.0,
        max_jerk=60.0,
    )

    # plot the waypoints
    mx, my = zip(*[(m.y, m.x) for m in points])
    plt.scatter(mx, my, c="r")

    # plot the trajectory
    x, y = zip(*[(seg.y, seg.x) for seg in trajectory])
    plt.plot(x, y)

    plt.xlabel('x variable')
    plt.ylabel('y variable')
    plt.title('Plot of Path Planning Algorithm')
    plt.show()