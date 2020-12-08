#include <math.h>
#include <stdio.h>

// User must define omega and v
// Calculating the normal force on each wheel

class WheelchairDynamics {

public:
static void compute(double theta_roll, double theta_pitch, double theta_3, double theta_4, double v,
   double v_dot, double omega, double omega_dot, double &torque_1, double &torque_2) {

     // Default values
     // Origin refers to midpoint between the two drive wheels
     double a = 0.195655; // X dist from origin to castor (m)
     double b = 0.658;    // Y dist from origin to castor (m)
     double c = 0.288;    // X dist from origin to drive wheel (m)
     double r_c = 0.0405; // Dist from center of castor to pivot (m)
     double r_dw = 0.176; // Radius of drive wheel (m)
     double m = 202;      // Mass of wheelchair (kg) (estimated)
     double n = 100;      // Ratio in stiffness between front and back wheels (estimated)
     double mu_rc = 0.004; // Coef of Rolling friction of castor (Value taken as bycicle tire on asphalt)
     double mu_rd = 0.004; // Coef of Rolling friction of drive wheel (Value taken as bicycle tire on asphalt)
     double mu_tau = 0.0155; // Coef of friction to pivot castor in place - taken as torque
                     // Estimated as 1/2 * thickness of wheel/2 * (Coef of friction = 1)
     double I = 22; // Taken from mesh model and scaled to match total mass. (N*m^2)

     double O_x = 0.00176;
     double O_y = -0.18841;
     double O_z = 0.21625; // (m) Values taken from COM of mesh body in Unreal

     double epsilon = 0.03;

     double g = 9.8;

double a_3 = a + r_c * cos(theta_3);
double a_4 = a + r_c * cos(theta_4);
double b_3 = b - r_c * sin(theta_3);
double b_4 = b - r_c * sin(theta_4);

double z_o = m*(g*(-n*pow(a_3*b_3 - a_4*b_4, 2) + (pow(b_3, 2) + pow(b_4, 2))
  *(pow(a_3, 2)*n + pow(a_4, 2)*n + 2*pow(c, 2)))*cos(theta_pitch)
  *cos(theta_roll) + n*((a_3 - a_4)*(pow(b_3, 2) + pow(b_4, 2))
  - (b_3 + b_4)*(a_3*b_3 - a_4*b_4))*(O_x*g*cos(theta_pitch)*cos(theta_roll)
  + O_z*g*sin(theta_pitch) + O_z*omega_dot) + (n*(a_3 - a_4)*(a_3*b_3 - a_4*b_4)
  - (b_3 + b_4)*(pow(a_3, 2)*n + pow(a_4, 2)*n + 2*pow(c, 2)))
  *(-O_y*g*cos(theta_pitch)*cos(theta_roll) + pow(O_z, 2)*v_dot + O_z*g
  *sin(theta_roll)*cos(theta_pitch)))/((pow(n, 2)*pow(a_3 - a_4, 2)
  *(pow(b_3, 2) + pow(b_4, 2)) - 2*pow(n, 2)*(a_3 - a_4)*(b_3 + b_4)
  *(a_3*b_3 - a_4*b_4) + n*pow(b_3 + b_4, 2)*(pow(a_3, 2)*n + pow(a_4, 2)
  *n + 2*pow(c, 2)) + 2*n*(n + 1)*pow(a_3*b_3 - a_4*b_4, 2) - 2*(pow(b_3, 2)
  + pow(b_4, 2))*(n + 1)*(pow(a_3, 2)*n + pow(a_4, 2)*n + 2*pow(c, 2))));

double theta = m*(-g*n*((a_3 - a_4)*(pow(b_3, 2) + pow(b_4, 2)) - (b_3 + b_4)*(a_3*b_3 - a_4*b_4))*cos(theta_pitch)*cos(theta_roll) + (n*pow(b_3 + b_4, 2) - 2*(pow(b_3, 2) + pow(b_4, 2))*(n + 1))*(O_x*g*cos(theta_pitch)*cos(theta_roll) + O_z*g*sin(theta_pitch) + O_z*omega_dot) + (n*(a_3 - a_4)*(b_3 + b_4) - 2*(n + 1)*(a_3*b_3 - a_4*b_4))*(-O_y*g*cos(theta_pitch)*cos(theta_roll) + pow(O_z, 2)*v_dot + O_z*g*sin(theta_roll)*cos(theta_pitch)))/((pow(n, 2)*pow(a_3 - a_4, 2)*(pow(b_3, 2) + pow(b_4, 2)) - 2*pow(n, 2)*(a_3 - a_4)*(b_3 + b_4)*(a_3*b_3 - a_4*b_4) + n*pow(b_3 + b_4, 2)*(pow(a_3, 2)*n + pow(a_4, 2)*n + 2*pow(c, 2)) + 2*n*(n + 1)*pow(a_3*b_3 - a_4*b_4, 2) - 2*(pow(b_3, 2) + pow(b_4, 2))*(n + 1)*(pow(a_3, 2)*n + pow(a_4, 2)*n + 2*pow(c, 2))));

double phi = m*(-g*n*(n*(a_3 - a_4)*(a_3*b_3 - a_4*b_4) - (b_3 + b_4)*(pow(a_3, 2)*n + pow(a_4, 2)*n + 2*pow(c, 2)))*cos(theta_pitch)*cos(theta_roll) - n*(-n*(a_3 - a_4)*(b_3 + b_4) + 2*(n + 1)*(a_3*b_3 - a_4*b_4))*(O_x*g*cos(theta_pitch)*cos(theta_roll) + O_z*g*sin(theta_pitch) + O_z*omega_dot) + (pow(n, 2)*pow(a_3 - a_4, 2) - 2*(n + 1)*(pow(a_3, 2)*n + pow(a_4, 2)*n + 2*pow(c, 2)))*(-O_y*g*cos(theta_pitch)*cos(theta_roll) + pow(O_z, 2)*v_dot + O_z*g*sin(theta_roll)*cos(theta_pitch)))/(n*(pow(n, 2)*pow(a_3 - a_4, 2)*(pow(b_3, 2) + pow(b_4, 2)) - 2*pow(n, 2)*(a_3 - a_4)*(b_3 + b_4)*(a_3*b_3 - a_4*b_4) + n*pow(b_3 + b_4, 2)*(pow(a_3, 2)*n + pow(a_4, 2)*n + 2*pow(c, 2)) + 2*n*(n + 1)*pow(a_3*b_3 - a_4*b_4, 2) - 2*(pow(b_3, 2) + pow(b_4, 2))*(n + 1)*(pow(a_3, 2)*n + pow(a_4, 2)*n + 2*pow(c, 2))));

double N_1 = -c*theta - z_o;

double N_2 = c*theta - z_o;

double N_3 = -a_3*n*theta + b_3*n*phi - n*z_o;

double N_4 = a_4*n*theta + b_4*n*phi - n*z_o;

double s_f3;
if (pow(b, 2)*pow(omega, 2) + pow(-a*omega + v, 2) < epsilon) {
   s_f3 = 0;
}
else {
   s_f3 = (b*omega*cos(theta_3) + (-a*omega + v)*sin(theta_3))/sqrt(pow(b, 2)*pow(omega, 2) + pow(a*omega - v, 2));
}

double s_t3;
if (pow(b, 2)*pow(omega, 2) + pow(-a*omega + v, 2) < epsilon) {
   s_t3 = 0;
}
else {
   s_t3 = (-b*r_c*omega*sin(theta_3) + r_c*(-a*omega + v)*cos(theta_3))/(r_c*sqrt(pow(b, 2)*pow(omega, 2) + pow(-a*omega + v, 2)));
}

double s_f4;
if (pow(b, 2)*pow(omega, 2) + pow(a*omega + v, 2) < epsilon) {
   s_f4 = 0;
}
else {
   s_f4 = (b*omega*cos(theta_4) + (a*omega + v)*sin(theta_4))/sqrt(pow(b, 2)*pow(omega, 2) + pow(a*omega + v, 2));
}

double s_t4;
if (pow(b, 2)*pow(omega, 2) + pow(-a*omega + v, 2) < epsilon) {
   s_t4 = 0;
}
else {
   s_t4 = (-b*r_c*omega*sin(theta_4) + r_c*(a*omega + v)*cos(theta_4))/(r_c*sqrt(pow(b, 2)*pow(omega, 2) + pow(a*omega + v, 2)));
}

double R_3x = ((s_f3 > epsilon) ? (
   -N_3*mu_rc*cos(theta_3)
)
: ((s_f3 < -epsilon) ? (
   N_3*mu_rc*cos(theta_3)
)
: (
   0
))) + ((s_t3 < -epsilon) ? (
   -N_3*mu_tau*sin(theta_3)
)
: ((s_t3 > epsilon) ? (
   N_3*mu_tau*sin(theta_3)
)
: (
   0
)));

double R_3y = ((s_f4 > epsilon) ? (
   -N_4*mu_rc*sin(theta_4)
)
: ((s_f4 < -epsilon) ? (
   N_4*mu_rc*sin(theta_4)
)
: (
   0
))) + ((s_t4 < -epsilon) ? (
   N_4*mu_tau*cos(theta_4)
)
: ((s_t4 > epsilon) ? (
   -N_4*mu_tau*cos(theta_4)
)
: (
   0
)));

double R_4x = ((s_f4 > epsilon) ? (
   -N_4*mu_rc*cos(theta_4)
)
: ((s_f4 < -epsilon) ? (
   N_4*mu_rc*cos(theta_4)
)
: (
   0
))) + ((s_t4 < -epsilon) ? (
   -N_4*mu_tau*sin(theta_4)
)
: ((s_t4 > epsilon) ? (
   N_4*mu_tau*sin(theta_4)
)
: (
   0
)));

double R_4y = ((s_f4 > epsilon) ? (
   -N_4*mu_rc*sin(theta_4)
)
: ((s_f4 < -epsilon) ? (
   N_4*mu_rc*sin(theta_4)
)
: (
   0
))) + ((s_t4 < -epsilon) ? (
   N_4*mu_tau*cos(theta_4)
)
: ((s_t4 > epsilon) ? (
   -N_4*mu_tau*cos(theta_4)
)
: (
   0
)));

double alpha_1 = -1.0L/2.0L*(I*omega_dot + O_x*g*m*sin(theta_roll)*cos(theta_pitch) + O_y*g*m*sin(theta_pitch) - R_3x*b + R_3y*a + R_3y*c - R_4x*b - R_4y*a + R_4y*c - c*g*m*sin(theta_roll)*cos(theta_pitch) - c*m*v_dot)/c;

double alpha_2 = (1.0L/2.0L)*(I*omega_dot + O_x*g*m*sin(theta_roll)*cos(theta_pitch) + O_y*g*m*sin(theta_pitch) - R_3x*b + R_3y*a - R_4x*b - R_4y*a - c*(R_3y + R_4y - g*m*sin(theta_roll)*cos(theta_pitch) - m*v_dot))/c;

torque_1 = r_dw*(-((-c*omega + v > epsilon) ? (
   -N_1*mu_rd
)
: ((-c*omega + v < -epsilon) ? (
   N_1*mu_rd
)
: (
   0
))) - 1.0L/2.0L*(I*omega_dot + O_x*g*m*sin(theta_roll)*cos(theta_pitch) + O_y*g*m*sin(theta_pitch) - R_3x*b + R_3y*a + R_3y*c - R_4x*b - R_4y*a + R_4y*c - c*g*m*sin(theta_roll)*cos(theta_pitch) - c*m*v_dot)/c);

torque_2 = r_dw*(-((c*omega + v > epsilon) ? (
   -N_2*mu_rd
)
: ((c*omega + v < -epsilon) ? (
   N_1*mu_rd
)
: (
   0
))) + (1.0L/2.0L)*(I*omega_dot + O_x*g*m*sin(theta_roll)*cos(theta_pitch) + O_y*g*m*sin(theta_pitch) - R_3x*b + R_3y*a - R_4x*b - R_4y*a - c*(R_3y + R_4y - g*m*sin(theta_roll)*cos(theta_pitch) - m*v_dot))/c);
}
};

int main() {
  double torque_1, torque_2;
  WheelchairDynamics::compute(0, 0, 1.5, 1.5, 1, 1, 0, 0.1, torque_1, torque_2);
  printf("My results are: %.2f, %.2f \n", torque_1, torque_2);
  return 0;
}
