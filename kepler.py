import math
import numpy as np

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

        h = np.cross(r_vec, v_vec)
        e = np.cross(v_vec, h) / mu - r_vec / np.linalg.norm(r_vec)

        n = np.cross(np.transpose(np.array([0, 0, 1])), h)

        if np.dot(r_vec, v_vec) > 0:
                nu = np.arccos(np.dot(e, r_vec)/(np.linalg.norm(e) * np.linalg.norm(r_vec)))
        else:
                nu = 2 * np.pi - np.arccos(np.dot(e, r_vec)/(np.linalg.norm(e) * np.linalg.norm(r_vec)))

        inc = np.arccos(h[2] / np.linalg.norm(h))
        ecc = np.linalg.norm(e)
        E = 2 * np.arctan((np.tan(nu / 2)) / np.sqrt((1 + ecc) / (1 - ecc)))

        if n[1] >= 0:
                lon_asc = np.arccos(n[0] / np.linalg.norm(n))
        else:
                lon_asc = 2 * np.pi - np.arccos(n[0] / np.linalg.norm(n))

        if e[2] >= 0:
                arg_peri = np.arccos(np.dot(n, e) / (np.linalg.norm(n) * np.linalg.norm(e)))
        else:
                arg_peri = 2 * np.pi - np.arccos(np.dot(n, e) / (np.linalg.norm(n) * np.linalg.norm(e)))

        M = E - ecc * np.sin(E)

        sma = 1 / (2/np.linalg.norm(r_vec) - np.linalg.norm(v_vec)**2 / mu)
        sma = sma * 6.684587e-9 # convert to AU
        
        return {"a": sma,
                "e": ecc,
                "i": np.rad2deg(inc),
                "arg_peri": np.rad2deg(arg_peri),
                "lon_asc": np.rad2deg(lon_asc)}

