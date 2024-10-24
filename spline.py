import numpy as np
from polynomials import *
from hermite import *
from pose import Pose
import math

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


        def integrand(t):
            return np.sqrt(self.dx(t)**2 + self.dy(t)**2)

        self.length = integrate(0, 1, integrand)

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

        def integrand(t):
            return np.sqrt(self.dx(t)**2 + self.dy(t)**2)

        self.length = integrate(0, 1, integrand)
    
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
               h4.derive().evaluate(time) * self.vx1 + \
               h5.derive().evaluate(time) * self.x1 

    def dy(self, time):
        return h0.derive().evaluate(time) * self.y0 + \
               h1.derive().evaluate(time) * self.vy0 + \
               h2.derive().evaluate(time) * self.ay0 + \
               h3.derive().evaluate(time) * self.ay1 + \
               h4.derive().evaluate(time) * self.vy1 + \
               h5.derive().evaluate(time) * self.y1  

    def ddx(self, time):
        return h0.derive().derive().evaluate(time) * self.x0 + \
               h1.derive().derive().evaluate(time) * self.vx0 + \
               h2.derive().derive().evaluate(time) * self.ax0 + \
               h3.derive().derive().evaluate(time) * self.ax1 + \
               h4.derive().derive().evaluate(time) * self.vx1 + \
               h5.derive().derive().evaluate(time) * self.x1 

    def ddy(self, time):
        return h0.derive().derive().evaluate(time) * self.y0 + \
               h1.derive().derive().evaluate(time) * self.vy0 + \
               h2.derive().derive().evaluate(time) * self.ay0 + \
               h3.derive().derive().evaluate(time) * self.ay1 + \
               h4.derive().derive().evaluate(time) * self.vy1 + \
               h5.derive().derive().evaluate(time) * self.y1  

    def getPointAtTime(self, time):
        return self.x(time), self.y(time)

    def getHeadingAtTime(self, time):
        return np.arctan2(self.dy(time), self.dx(time))

    def getPoseAtTime(self, time):
        return Pose(self.getPointAtTime(time), self.getHeadingAtTime(time))

    def getLength(self): 
        return self.length

    def getCurvature(self, time): # can be optimized
        dx, dy = self.dx(time), self.dy(time)

        numerator = dx * self.ddy(time) - self.ddx(time) * self.dy(time)
        denom = (np.sqrt(dx** 2 + dy ** 2)) ** 3

        return numerator / denom

    def getVelocityReduction(self, time, scalar = 5): # find new name this stinks  
        clamped_curvature = np.abs(self.getCurvature(time))

        #return np.clip(-clamped_curvature * scalar + 1, 0, 1) # completly ignores splines length
        return np.clip((scalar - clamped_curvature * self.getLength()) / scalar, 0, 1) # respects length of spline