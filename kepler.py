import math
import numpy as np

# "stolen" from OrbitSim3D, modified for use with Numpy
# https://github.com/arda-guler/orbitSim3D/blob/master/orbit.py
def state2kepler(r_vec, v_vec):
        r = np.dot(r_vec, r_vec)
        v = np.dot(v_vec, v_vec)
        mu = 132712e6 # km3 s-2, Sol gravitational parameter

        # = = = DETERMINE KEPLER ELEMENTS = = =
        # sma: semi-major axis
        # e: eccentricity
        # arg_peri: argument of periapsis
        # inc: inclination
        # lon_asc: longitude/right ascension of ascending node

        v_r = np.dot(v_vec, r_vec/r)
        v_t = (v**2 - v_r**2)**0.5

        sma = 1/(2/r - v**2/mu)

        h_vec = np.cross(r_vec, v_vec)
        h = np.dot(h_vec, h_vec)

        inc = math.acos(h_vec[2] / h)

        K = np.array([0, 0, 1])
        N_vec = np.cross(K, h_vec)
        N = np.dot(N_vec, N_vec)

        if not N:
            if (r_vec[1] > 0 and v_vec[0] > 0) or (r_vec[1] < 0 and v_vec[0] < 0):
                lon_asc = math.pi * 1.5
            else:
                lon_asc = math.pi * 0.5

        else:
            lon_asc = math.acos(N_vec[0] / N)
            if N_vec[1] < 0:
                lon_asc = 2 * math.pi - lon_asc

        e_vec = np.cross(v_vec, h_vec) / mu - r_vec / r
        e = np.dot(e_vec, e_vec)

        if (N * e):
            arg_peri = math.acos(np.dot(N_vec, e_vec) / (N * e))
            if e_vec[2] < 0:
                arg_peri = 2 * math.pi - arg_peri
        else:
            arg_peri = math.pi * 0.5

        return {"a": sma,
                "e": e,
                "i": np.rad2deg(inc),
                "arg_peri": np.rad2deg(arg_peri),
                "lon_asc": np.rad2deg(lon_asc)}
