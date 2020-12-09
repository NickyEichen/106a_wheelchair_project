from wheelchair_controller import WheelchairController

robot = WheelchairController()

print(robot.calc_torques(2, 0))
