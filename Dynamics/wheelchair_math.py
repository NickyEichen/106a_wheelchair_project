import numpy as np
from numpy import cos, sin, sqrt, array, pi
import math

# Default values
# Origin refers to midpoint between the two drive wheels
a = 0.195655 # X dist from origin to castor (m)
b = 0.658    # Y dist from origin to castor (m)
c = 0.288    # X dist from origin to drive wheel (m)
r_c = 0.0405 # Dist from center of castor to pivot (m)
r_dw = 0.176 # Radius of drive wheel (m)
m = 202      # Mass of wheelchair (kg) (estimated)
n = 100      # Ratio in stiffness between front and back wheels (estimated)
mu_rc = 0.2 # Coef of Rolling friction of castor (Value taken as bycicle tire on asphalt)
mu_rd = 0 # Coef of Rolling friction of drive wheel (Value taken as bicycle tire on asphalt)
mu_tau = 1 # Coef of friction to pivot castor in place - taken as torque
                # Estimated as 1/2 * thickness of wheel/2 * (Coef of friction = 1)
Izz = 22 # Taken from mesh model and scaled to match total mass. (N*m^2)

O_x, O_y, O_z = 0.00176, -0.18841, 0.21625 # (m) Values taken from COM of mesh body in Unreal

epsilon = 0.035

def calc(roll, pitch, theta_3, theta_4, v, v_dot, omega, omega_dot, a=a, b=b, c=c, r_c=r_c, r_dw=r_dw, m=m, n=n, epsilon=epsilon, mu_rc=mu_rc, mu_rd=mu_rd, mu_tau=mu_tau,
         O_x=O_x, o_y = O_y, O_z = O_z, I=Izz):
    theta_pitch = pitch
    theta_roll = roll
    g = 9.8

    a_3 = a + r_c * cos(theta_3)
    a_4 = a + r_c * cos(theta_4)
    b_3 = b - r_c * sin(theta_3)
    b_4 = b - r_c * sin(theta_4)
    A_prime = array([[-2*n - 2, -n*(a_3 - a_4), n*(b_3 + b_4)], [n*(b_3 + b_4), n*(a_3*b_3 - a_4*b_4), -n*(b_3**2 + b_4**2)], [-n*(a_3 - a_4), -a_3**2*n - a_4**2*n - 2*c**2, n*(a_3*b_3 - a_4*b_4)]])
    B_prime = array([[-1, -c, 0], [-1, c, 0], [-n, -a_3*n, b_3*n], [-n, a_4*n, b_4*n]])
    L = array([[g*m*cos(theta_pitch)*cos(theta_roll)], [O_y*g*m*cos(theta_pitch)*cos(theta_roll) - O_z**2*m*v_dot - O_z*g*m*sin(theta_roll)*cos(theta_pitch)], [-O_x*g*m*cos(theta_pitch)*cos(theta_roll) - O_z*g*m*sin(theta_pitch) - O_z*m*omega_dot]])
    N_1, N_2, N_3, N_4 = B_prime.dot(np.linalg.inv(A_prime)).dot(L).T[0]
    s_f3 = (((b*omega*cos(theta_3) + (-a*omega + v)*sin(theta_3))/sqrt(b**2*omega**2 + (a*omega - v)**2)) if (b**2*omega**2 + (-a*omega + v)**2 > epsilon) else ((((b*cos(theta_3)*omega_dot + (-a*omega_dot + v_dot)*sin(theta_3))/sqrt(b**2*omega_dot**2 + (a*omega_dot - v_dot)**2)) if (b**2*omega_dot**2 + (-a*omega_dot + v_dot)**2 > epsilon) else (((0) if (True) else None)))))
    R_f3 = -1 * (((array([[-N_3*mu_rc*cos(theta_3)], [-N_3*mu_rc*sin(theta_3)], [0]])) if (s_f3 > epsilon) else (((array([[N_3*mu_rc*cos(theta_3)], [N_3*mu_rc*sin(theta_3)], [0]])) if (s_f3 < -epsilon) else (((array([[0], [0], [0]])) if (True) else None))))))
    s_t3 = (((-b*r_c*omega*sin(theta_3) + r_c*(-a*omega + v)*cos(theta_3))/(r_c*sqrt(b**2*omega**2 + (-a*omega + v)**2))) if (b**2*omega**2 + (-a*omega + v)**2 > epsilon) else ((((-b*r_c*sin(theta_3)*omega_dot + r_c*(-a*omega_dot + v_dot)*cos(theta_3))/(r_c*sqrt(b**2*omega_dot**2 + (-a*omega_dot + v_dot)**2))) if (b**2*omega_dot**2 + (-a*omega_dot + v_dot)**2 > epsilon) else (((0) if (True) else None)))))
    R_tau_3 = -1 * ((array([[-N_3*mu_tau*sin(theta_3)], [N_3*mu_tau*cos(theta_3)], [0]])) if (s_t3 < -epsilon) else (((array([[N_3*mu_tau*sin(theta_3)], [-N_3*mu_tau*cos(theta_3)], [0]])) if (s_t3 > epsilon) else (((array([[0], [0], [0]])) if (True) else None)))))
    R_3 = R_f3 + R_tau_3
    R_3x, R_3y, _ = R_3.T[0]
    s_f4 = (((b*omega*cos(theta_4) + (a*omega + v)*sin(theta_4))/sqrt(b**2*omega**2 + (a*omega + v)**2)) if (b**2*omega**2 + (a*omega + v)**2 > epsilon) else ((((b*cos(theta_4)*omega_dot + (a*omega_dot + v_dot)*sin(theta_4))/sqrt(b**2*omega_dot**2 + (a*omega_dot + v_dot)**2)) if (b**2*omega_dot**2 + (a*omega_dot + v_dot)**2 > epsilon) else (((0) if (True) else None)))))
    R_f4 = -1 * ((array([[-N_4*mu_rc*cos(theta_4)], [-N_4*mu_rc*sin(theta_4)], [0]])) if (s_f4 > epsilon) else (((array([[N_4*mu_rc*cos(theta_4)], [N_4*mu_rc*sin(theta_4)], [0]])) if (s_f4 < -epsilon) else (((array([[0], [0], [0]])) if (True) else None)))))
    s_t4 = (((-b*r_c*omega*sin(theta_4) + r_c*(a*omega + v)*cos(theta_4))/(r_c*sqrt(b**2*omega**2 + (a*omega + v)**2))) if (b**2*omega**2 + (a*omega + v)**2 > epsilon) else ((((-b*r_c*sin(theta_4)*omega_dot + r_c*(a*omega_dot + v_dot)*cos(theta_4))/(r_c*sqrt(b**2*omega_dot**2 + (a*omega_dot + v_dot)**2))) if (b**2*omega_dot**2 + (a*omega_dot + v_dot)**2 > epsilon) else (((0) if (True) else None)))))
    R_tau_4 = -1 * ((array([[-N_4*mu_tau*sin(theta_4)], [N_4*mu_tau*cos(theta_4)], [0]])) if (s_t4 < -epsilon) else (((array([[N_4*mu_tau*sin(theta_4)], [-N_4*mu_tau*cos(theta_4)], [0]])) if (s_t4 > epsilon) else (((array([[0], [0], [0]])) if (True) else None)))))
    R_4 = R_f4 + R_tau_4
    R_4x, R_4y, _ = R_4.T[0]
    alpha_1 = -(I*omega_dot + O_x*g*m*sin(theta_roll)*cos(theta_pitch) + O_y*g*m*sin(theta_pitch) - R_3x*b + R_3y*a + R_3y*c - R_4x*b - R_4y*a + R_4y*c - c*g*m*sin(theta_roll)*cos(theta_pitch) - c*m*v_dot)/(2*c)
    alpha_2 = (I*omega_dot + O_x*g*m*sin(theta_roll)*cos(theta_pitch) + O_y*g*m*sin(theta_pitch) - R_3x*b + R_3y*a - R_4x*b - R_4y*a - c*(R_3y + R_4y - g*m*sin(theta_roll)*cos(theta_pitch) - m*v_dot))/(2*c)
    torque_1 = r_dw*(-((-N_1*mu_rd) if (-c*omega + v > epsilon) else (((N_1*mu_rd) if (-c*omega + v < -epsilon) else (((0) if (True) else None))))) - (I*omega_dot + O_x*g*m*sin(theta_roll)*cos(theta_pitch) + O_y*g*m*sin(theta_pitch) - R_3x*b + R_3y*a + R_3y*c - R_4x*b - R_4y*a + R_4y*c - c*g*m*sin(theta_roll)*cos(theta_pitch) - c*m*v_dot)/(2*c))
    torque_2 = r_dw*(-((-N_2*mu_rd) if (c*omega + v > epsilon) else (((N_1*mu_rd) if (c*omega + v < -epsilon) else (((0) if (True) else None))))) + (I*omega_dot + O_x*g*m*sin(theta_roll)*cos(theta_pitch) + O_y*g*m*sin(theta_pitch) - R_3x*b + R_3y*a - R_4x*b - R_4y*a - c*(R_3y + R_4y - g*m*sin(theta_roll)*cos(theta_pitch) - m*v_dot))/(2*c))

    d = {'N1': N_1, 'N2': N_2, 'N3': N_3, 'N4': N_4, 'sf3': s_f3, 'sf4': s_f4, 'st3': s_t3, 'st4': s_t4,
         #'R3f': (R_f3[0,0], R_f3[1,0]), 'R3t': (R_tau_3[0,0], R_tau_3[1,0]), 'R4f': (R_f4[0,0], R_f4[1,0]), 'R4t': (R_tau_4[0,0], R_tau_4[1,0]),
         'R3x': R_3x, 'R3y': R_3y, 'R4x': R_4x, 'R4y': R_4y, 'a1': alpha_1, 'a2': alpha_2, 'torque_1': torque_1, 'torque_2': torque_2}
    return d

def calc_velocities(left_wheel_speed, right_wheel_speed):
    lin_vel = (left_wheel_speed + right_wheel_speed) / 2
    ang_vel = ( - left_wheel_speed + right_wheel_speed) / (2*c)
    return lin_vel, ang_vel

def calcsimp(v, vdot, o, odot, t3=1.5, t4=1.5):
    return calc_simplified(0, 0, t3*np.pi, t4*np.pi, v, vdot, o, odot)

def set_a(x):
    a = x
def set_b(x):
    b = x
def set_c(x):
    c = x
def set_castor_dist(x):
    r_c = x
def set_drive_wheel_radius(x):
    r_dw = x
def set_mass(x):
    m = x
def set_spring_ratio(x):
    n = x
def set_mu_rc(x):
    mu_rc = x
def set_mu_rd(x):
    mu_rd = x
def set_mu_tau(x):
    mu_tau = x
def set_COM(x, y, z):
    O_x = x
    O_y = y
    O_z = z
def set_epsilon(x):
    epsilon = x


#simplified version to demo driving in straight lines
def calc_simplified(roll, pitch, theta_3, theta_4, v, v_dot, omega, omega_dot):

    castor_drive_fric = 20
    castor_rot_fric = 240
    t_look_ahead = 1.5

    vel_thresh = 0.2
    omega_thresh = 0.2

    v_future = v + v_dot*(t_look_ahead**2) /2
    omega_future = omega + omega_dot*(t_look_ahead**2) /2

    if (abs(v_future) > vel_thresh  or abs(omega_future) > omega_thresh):
        t3_ideal = math.atan2(v_future - a*omega_future, b*omega_future)
        t4_ideal = math.atan2(v_future + a*omega_future, b*omega_future)
    else:
        #print("v_future: % .2f, omega_future: % .2f" %(v_future, omega_future))
        return (0, 0)
    t3_ideal = rad_norm(t3_ideal + pi)
    t4_ideal = rad_norm(t4_ideal + pi)

    #print("Ideal thetas: ", t3_ideal*180/pi, t4_ideal*180/pi)

    T = omega_dot * Izz
    F = v_dot * m
    er3 = rad_norm(t3_ideal - theta_3)
    if (er3 < -epsilon):
        c_val = cos(theta_3 - pi/2)
        s_val = sin(theta_3 - pi/2)
        T -= castor_rot_fric * (c_val*b - s_val*a)
        F -= castor_rot_fric * s_val
    elif er3 > epsilon:
        c_val = cos(theta_3 + pi/2)
        s_val = sin(theta_3 + pi/2)
        T -= castor_rot_fric * (c_val*b - s_val*a)
        F -= castor_rot_fric * s_val
    if abs(er3) < pi/2:
        c_val = cos(theta_3)
        s_val = sin(theta_3)
        T -= castor_drive_fric * (c_val*b - s_val*a)
        F -= castor_drive_fric * s_val
    else:
        c_val = cos(theta_3)
        s_val = sin(theta_3)
        T += castor_drive_fric * (c_val*b - s_val*a)
        F += castor_drive_fric * s_val

    er4 = rad_norm(t4_ideal - theta_4)
    if (er4< -epsilon):
        c_val = cos(theta_4 - pi/2)
        s_val = sin(theta_4 - pi/2)
        T -= castor_rot_fric * (c_val*b + s_val*a)
        F -= castor_rot_fric * s_val
    elif er3 > epsilon:
        c_val =  cos(theta_4 + pi/2)
        s_val = sin(theta_4 + pi/2)
        T -= castor_rot_fric * (c_val*b + s_val*a)
        F -= castor_rot_fric * s_val
    if abs(er4) < pi/2:
        c_val = cos(theta_4)
        s_val = sin(theta_4)
        T -= castor_drive_fric * (c_val*b + s_val*a)
        F -= castor_drive_fric * s_val
    else:
        c_val = cos(theta_4)
        s_val = sin(theta_4)
        T += castor_drive_fric * (c_val*b - s_val*a)
        F += castor_drive_fric * s_val
    #print("Foward force: %.3f, Turning Torque: %.3f" %(F, T))

    torque_1 = (F - T/c) * r_dw
    torque_2 = (F + T/c) * r_dw
    return torque_1, torque_2

def rad_norm(n):
    if n > pi:
        return rad_norm(n - 2*pi)
    elif n < -pi:
        return rad_norm(n + 2*pi)
    return n
