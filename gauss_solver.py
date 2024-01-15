import numpy as np
import math

from JPLHorizons import get_earth_position_vector
from kepler import state2kepler

PI = math.pi
PI_12 = PI/12
PI_720 = PI/720
PI_43200 = PI/43200

class RightAscension:
    def __init__(self, h, m, s):
        self.neg = False
        if h < 0:
            self.neg = True
            
        self.h = abs(h)
        self.m = m
        self.s = s

    def toRad(self):
        if not self.neg:
            return self.h * PI_12 + self.m * PI_720 + self.s * PI_43200
        else:
            return -self.h * PI_12 - self.m * PI_720 - self.s * PI_43200

    def toDeg(self):
        # won't bother, this works
        return math.degrees(self.toRad())

class Declination:
    def __init__(self, d, m, s):
        self.neg = False
        if d < 0:
            self.neg = True
            
        self.d = abs(d)
        self.m = m
        self.s = s

    def toRad(self):
        deg_decimal = self.d + self.m / 60 + self.s / 3600
        if self.neg:
            deg_decimal = -deg_decimal
        return math.radians(deg_decimal)

    def toDeg(self):
        return self.d + self.m / 60 + self.s / 3600

class Observation:
    def __init__(self, RA, DEC, time, datetime):
        self.RA = RA.toDeg()
        self.DEC = DEC.toDeg()
        self.time = time
        self.datetime = datetime

def sind(x):
    return np.sin(np.radians(x))

def cosd(x):
    return np.cos(np.radians(x))

def dist_poly_solver(a, b, c, tolerance=1e-4, maxiter=1e8, relaxation=0.0005):
    
    def f(x):
        return x**8 + a*x**6 + b*x**3 + c

    def df(x):
        return 8*x**7 + a*6*x**5 + 3*b*x**2

    x = 100000  # this is a bloody random initial value
                # discovered to usually work with trial and error
    error = tolerance * 1e8
    itercount = 0

    while error > tolerance and itercount < maxiter:
        x = x - f(x)/df(x) * relaxation
        error = f(x)
        
        itercount += 1
        if itercount % 1e2 == 0:
            print("Newton-Raphson solver is working...")
            print("Iteration:", itercount, "error:", error, "x:", x)
            print("")

    if itercount == maxiter:
        print("Did not converge!")

    return x

def gauss(obs1, obs2, obs3, Rs=None):
    mu = 132712e6 # km3 s-2, Sol gravitational parameter

    if not Rs:
        # This uses JPL Horizons API
        R1 = np.array(get_earth_position_vector(obs1.datetime))
        R2 = np.array(get_earth_position_vector(obs2.datetime))
        R3 = np.array(get_earth_position_vector(obs3.datetime))

    else:
        R1 = Rs[0]
        R2 = Rs[1]
        R3 = Rs[2]

    # the part below is explained neatly on Wikipedia
    # https://en.wikipedia.org/wiki/Gauss%27s_method
    t1 = obs1.time
    t2 = obs2.time
    t3 = obs3.time

    tau1 = t1 - t2
    tau3 = t3 - t2
    tau = t3 - t1

    rho1 = np.array([cosd(obs1.DEC) * cosd(obs1.RA),
                     cosd(obs1.DEC) * sind(obs1.RA),
                     sind(obs1.DEC)])

    rho2 = np.array([cosd(obs2.DEC) * cosd(obs2.RA),
                     cosd(obs2.DEC) * sind(obs2.RA),
                     sind(obs2.DEC)])

    rho3 = np.array([cosd(obs3.DEC) * cosd(obs3.RA),
                     cosd(obs3.DEC) * sind(obs3.RA),
                     sind(obs3.DEC)])

    p1 = np.cross(rho2, rho3)
    p2 = np.cross(rho1, rho3)
    p3 = np.cross(rho1, rho2)

    D0 = np.dot(rho1, p1)

    D11 = np.dot(R1, p1)
    D12 = np.dot(R1, p2)
    D13 = np.dot(R1, p3)

    D21 = np.dot(R2, p1)
    D22 = np.dot(R2, p2)
    D23 = np.dot(R2, p3)

    D31 = np.dot(R3, p1)
    D32 = np.dot(R3, p2)
    D33 = np.dot(R3, p3)

    A = (1/D0) * (-D12 * tau3/tau + D22 + D32 * tau1/tau)
    B = 1/(6 * D0) * (D12 * (tau3**2 - tau**2) * tau3/tau + D32 * (tau**2 - tau1**2) * tau1/tau)
    E = np.dot(R2, rho2)

    R2_sqr = np.dot(R2, R2)

    lc_a = -(A**2 + 2*A*E + R2_sqr)
    lc_b = -2*mu*B*(A+E)
    lc_c = -mu**2 * B**2

    lc_r2 = dist_poly_solver(lc_a, lc_b, lc_c)

    # slant range
    nv_rho1 = 1/D0 * ((6 * (D31 * tau1/tau3 + D21 * tau/tau3) * lc_r2**3 + mu * D31 * (tau**2 - tau1**2) * tau1/tau3) / (6*lc_r2**3 + mu * (tau**2 - tau3**2)) - D11)
    nv_rho2 = A + mu*B/lc_r2**3
    nv_rho3 = 1/D0 * ((6 * (D13 * tau3/tau1 - D23 * tau/tau1) * lc_r2**3 + mu * D13 * (tau**2 - tau3**2) * tau3/tau1) / (6*lc_r2**3 + mu*(tau**2 - tau1**2)) - D33)

    yv_r1 = R1 + nv_rho1 * rho1
    yv_r2 = R2 + nv_rho2 * rho2
    yv_r3 = R3 + nv_rho3 * rho3

    f1 = 1 - 0.5 * mu/lc_r2**3 * tau1**2
    f3 = 1 - 0.5 * mu/lc_r2**3 * tau3**2
    g1 = tau1 - 1/6 * mu/lc_r2**3 * tau1**3
    g3 = tau3 - 1/6 * mu/lc_r2**3 * tau3**3

    vel2 = 1/(f1*g3 - f3*g1) * (-f3 * yv_r1 + f1 * yv_r3)

    # return yv_r2, vel2 # returns position vector and velocity vector for second observation (km, km/s)

    orbital_elements = state2kepler(yv_r2, vel2)
    return orbital_elements
