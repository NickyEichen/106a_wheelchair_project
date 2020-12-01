
import wheelchair_math as WC_Math
import math

class WheelchairController:
    def __init__(self):

        # Driver Control Coefficients
        self._velcontrol_lin_Kv = 0.1
        self._velcontrol_ang_Kv = 0.1

        self._max_linear_vel = 3
        self._max_angular_vel = 2.5
        self._max_linear_acel = 1
        self._max_angular_acel = 0.5


        self._roll = 0
        self._pitch = 0
        self._left_castor_angle = math.pi*3/2
        self._right_castor_angle = math.pi*3/2
        self._linear_velocity = 0
        self._angular_orientation = 0
        self._angular_velocity = 0

        #Not currently used, but might be useful if we want to add features.
        self._dynamic_states = {}

        #Set up any listeners / services / other stuff

    def update_states():
        #Update self._ ... for all state variables above
        # Verify that _roll is around the positive x axis and
        #_yaw is around positive y axis where Y AXIS is the direction the wheelchair drives
        self._up_to_date = False
        return

    def calc_torques(self, linear_acel, angular_acel):
        self._dynamic_states = WC_Math.calc(self._roll, self._pitch, self._left_castor_angle, self._right_castor_angle,
                            self._linear_velocity, linear_acel, self._angular_velocity, angular_acel)
        return self._dynamic_states['torque_1'], self._dynamic_states['torque_2']

    def velocity_control(self, linear_vel, angular_vel, linear_acel=0, angular_acel=0):
        """
        Takes a desired linear velocity LINEAR_VEL and angular velocity ANGULAR_VEL.
        Performs proportional computed torque control to match.
        Limits maximum acceleration and maximum velocity for safety of the riders.
        """

        # Calculate linear acceleration, with proper limits
        if abs(self._linear_velocity) < self._max_linear_vel:
            lin_acel = linear_acel + (self._linear_velocity - linear_vel) * self._velcontrol_lin_Kv
            lin_acel = max(min(lin_acel, self._max_linear_acel), -self._max_linear_acel)
        else:
            lin_acel = 0

        # Calculate angular aceleration with proper limits
        if abs(self._angular_velocity) < self._max_angular_vel:
            ang_acel = angular_acel + (self._angular_velocity - angular_vel) * self._velcontrol_ang_Kv
            ang_acel = max(min(ang_acel, self._max_angular_acel), -self._max_angular_acel)
        else:
            ang_acel = 0

        # Convert acelerations into torques    
        return self.calc_torques(lin_acel, ang_acel)


if __name__ == "__main__":
    robot = WheelchairController()
    print(robot.calc_torques(1, 0))
