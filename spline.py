import numpy as np
from polynomials import *
from hermite import *
from pose import Pose

class Spline:
    def __init__(self, x0, y0, x1, y1, t0, t1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.t0 = t0
        self.t1 = t1
        self.d = np.sqrt((x1-x0)**2 + (y1-y0)**2)

        self.vx0 = np.cos(t0) * self.d
        self.vy0 = np.sin(t0) * self.d

        self.vx1 = np.cos(t1) * self.d
        self.vy1 = np.sin(t1) * self.d

        # Acceraltion Points unused
        self.ax0, self.ay0, self.ax1, self.ay1 = 0, 0, 0, 0

    def __init__(self, p0, p1, t0, t1):
        self.x0, self.y0 = p0
        self.x1, self.y1 = p1
        self.t0 = t0
        self.t1 = t1
        self.d = np.sqrt((self.x1-self.x0)**2 + (self.y1-self.y0)**2)

        self.vx0 = np.cos(t0) * self.d
        self.vy0 = np.sin(t0) * self.d

        self.vx1 = np.cos(t1) * self.d
        self.vy1 = np.sin(t1) * self.d

        # Acceraltion Points unused
        self.ax0, self.ay0, self.ax1, self.ay1 = 0, 0, 0, 0

    def spit(self):
        print(f"d = {self.d}")
        print(f"vx0 = {self.vx0}")
        print(f"vy0 = {self.vy0}")
        print(f"vx1 = {self.vx1}")
        print(f"vy1 = {self.vy1}")
    
    def x(self, time):
        return h0.evaluate(time) * self.x0 + \
               h1.evaluate(time) * self.vx0 + \
               h2.evaluate(time) * self.ax0 + \
               h3.evaluate(time) * self.ax1 + \
               h4.evaluate(time) * self.vx1 + \
               h5.evaluate(time) * self.x1  

    def y(self, time):
        return h0.evaluate(time) * self.y0 + \
               h1.evaluate(time) * self.vy0 + \
               h2.evaluate(time) * self.ay0 + \
               h3.evaluate(time) * self.ay1 + \
               h4.evaluate(time) * self.vy1 + \
               h5.evaluate(time) * self.y1  

    def dx(self, time):
        return h0.derive().evaluate(time) * self.x0 + \
               h1.derive().evaluate(time) * self.vx0 + \
               h2.derive().evaluate(time) * self.ax0 + \
               h3.derive().evaluate(time) * self.ax1 + \
               h4.derive().evaluate(time) * self.vx0 + \
               h5.derive().evaluate(time) * self.x1 

    def dy(self, time):
        return h0.derive().evaluate(time) * self.y0 + \
               h1.derive().evaluate(time) * self.vy0 + \
               h2.derive().evaluate(time) * self.ay0 + \
               h3.derive().evaluate(time) * self.ay1 + \
               h4.derive().evaluate(time) * self.vy0 + \
               h5.derive().evaluate(time) * self.y1  

    def getPointAtTime(self, time):
        return self.x(time), self.y(time)

    def getHeadingAtTime(self, time):
        return self.dy(time) / self.dx(time)

    def getPoseAtTime(self, time):
        return Pose(self.getPointAtTime(time), self.getHeadingAtTime(time))




