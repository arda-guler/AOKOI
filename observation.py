import math
import numpy as np
import datetime

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

    def __repr__(self):
        out = "RA: " + str(self.h) + " " + str(self.m) + " " + str(self.s)
        return out

    def __str__(self):
        out = str(self.h) + " " + str(self.m) + " " + str(self.s)
        return out

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

    def __repr__(self):
        if self.neg:
            out = "DEC: -" + str(self.d) + " " + str(self.m) + " " + str(self.s)
        else:
            out = "DEC: +" + str(self.d) + " " + str(self.m) + " " + str(self.s)
        return out

    def __str__(self):
        if self.neg:
            out = "-" + str(self.d) + " " + str(self.m) + " " + str(self.s)
        else:
            out = "+" + str(self.d) + " " + str(self.m) + " " + str(self.s)
        return out

    def toRad(self):
        deg_decimal = self.d + self.m / 60 + self.s / 3600
        if self.neg:
            deg_decimal = -deg_decimal
        return math.radians(deg_decimal)

    def toDeg(self):
        if not self.neg:
            return self.d + self.m / 60 + self.s / 3600
        else:
            return -1 * (self.d + self.m / 60 + self.s / 3600)

class Observation:
    def __init__(self, name, RA, DEC, date_time, mag):
        self.name = name
        self.RA = RA
        self.DEC = DEC
        self.date_time = date_time
        self.mag = mag

    def __repr__(self):
        out = "Obs: " + str(self.date_time) + " " + str(self.RA) + " " + str(self.DEC) + " " + str(self.mag)
        return out

class MPCDate:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day_orig = day
        self.day = int(day)

        self.hour = int((day - int(day)) * 24)
        self.minute = int((day - int(day) - self.hour/24) * 24 * 60)
        self.second = int((day - int(day) - self.hour/24 - self.minute/(24*60)) * 24 * 60 * 60)

    def __str__(self):
        month_str = str(self.month)
        if self.month < 10:
            month_str = "0" + month_str

        day_str = str(self.day_orig)
        if self.day < 10:
            day_str = "0" + day_str
            
        out = str(self.year) + " " + month_str + " " + day_str
        return out

    def str_precise(self):
        month_str = str(self.month)
        if self.month < 10:
            month_str = "0" + month_str

        day_str = str(self.day)
        if self.day < 10:
            day_str = "0" + day_str

        hour_str = str(self.hour)
        if self.hour < 10:
            hour_str = "0" + hour_str

        minute_str = str(self.minute)
        if self.minute < 10:
            minute_str = "0" + minute_str
            
        datestr = str(self.year) + "-" + month_str + "-" + day_str + " " + hour_str + ":" + minute_str
        return datestr

    def MPC2datetime(self):
        month_str = str(self.month)
        if self.month < 10:
            month_str = "0" + month_str

        day_str = str(self.day)
        if self.day < 10:
            day_str = "0" + day_str

        hour_str = str(self.hour)
        if self.hour < 10:
            hour_str = "0" + hour_str

        minute_str = str(self.minute)
        if self.minute < 10:
            minute_str = "0" + minute_str

        second_str = str(self.second)
        if self.second < 10:
            second_str = "0" + second_str
            
        datestr = str(self.year) + "-" + month_str + "-" + day_str + " " + hour_str + ":" + minute_str + ":" + second_str
        return datetime.datetime.fromisoformat(datestr)
