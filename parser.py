from observation import *

def MPC80Parser(m):
    try:
        name = m[5:12]
        
        date_year = m[15:19]
        date_month = m[20:22]
        date_day = m[23:31]

        RA = m[32:43]
        DEC = m[44:55]

        try:
            mag = float(m[65:69])
        except:
            mag = 0

        RA = RA.split(" ")
        RA = RightAscension(int(RA[0]), int(RA[1]), float(RA[2]))

        DEC = DEC.split(" ")
        DEC = Declination(int(DEC[0]), int(DEC[1]), float(DEC[2]))

        date = MPCDate(int(date_year), int(date_month), float(date_day))

        obs = Observation(name, RA, DEC, date, mag)
        
        return obs
    except:
        print("Could not parse line:", m)
        return None
