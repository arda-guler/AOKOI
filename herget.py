import numpy as np

from observation import *
from kepler import *
from JPLHorizons import *
from parser import *

def sind(x):
    return np.sin(np.radians(x))

def cosd(x):
    return np.cos(np.radians(x))

def herget(obs1, obs2, R, Es = None):
    AU = 1.495979e8
    mu = 132712e6

    r1 = R
    r2 = R

    if not Es:
        E1 = np.array(get_earth_position_vector(str(obs1.date_time)))
        E2 = np.array(get_earth_position_vector(str(obs2.date_time)))
    else:
        E1 = Es[0]
        E2 = Es[1]
    
    t1 = obs1.date_time.MPC2datetime()
    t2 = obs2.date_time.MPC2datetime()

    delta_t = (t2 - t1).total_seconds()

    rho1 = np.array([r1 * cosd(obs1.RA.toDeg()) * cosd(obs1.DEC.toDeg()),
                     r1 * sind(obs1.RA.toDeg()) * cosd(obs1.DEC.toDeg()),
                     r1 * sind(obs1.DEC.toDeg())])

    rho2 = np.array([r2 * cosd(obs2.RA.toDeg()) * cosd(obs2.DEC.toDeg()),
                     r2 * sind(obs2.RA.toDeg()) * cosd(obs2.DEC.toDeg()),
                     r2 * sind(obs2.DEC.toDeg())])

    p1 = E1 + rho1
    p2 = E2 + rho2

    p = p1

    # initial guess
    v1 = (p2 - p1) / delta_t

    pmid = (p1 + p2) * 0.5
    amid = mu * pmid / (np.linalg.norm(pmid)**3)

    # v1 = (p2 - p1) / delta_t - amid * delta_t / 2

    K = 1
    h = delta_t / 1000
    delta = 10 * AU
    attempts = 1
    while delta > 0.0002 * AU:
        v = v1
        p = p1
        for i in range(1000):
            v = v - mu * p / (np.linalg.norm(p)**3) * h
            p = p + v * h

        delta = np.linalg.norm(p2 - p)
        v1 = v1 + (p2 - p) * K / delta_t
        attempts += 1

        if attempts % 100 == 0:
            K *= 0.2

    oe = state2kepler(p1, v)
    return oe
