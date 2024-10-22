from pose import Pose
from cordconversion import toField, toScreen
from polynomials import *
from spline import Spline
import numpy as np

class Trajectory:
    def __init__(self, path):
        self.path = path
        self.splines = self.compute()

    def getPoseAtTime(self, time):
        baseTime = int(np.ceil(time))
        currentSpline = self.splines[baseTime - 1]
        parametrizedTime = baseTime - time

        return currentSpline.getPoseAtTime(parametrizedTime)

    def getHeadingAtTime(self, time):
        return self.getPoseAtTime(time).heading()

    def getDuration(self): # rename
        return len(self.splines)

    def drawTrajectory(self, pygame, screen, resolution = 1): # TODO: make it not draw every single frame, and only on update
        for time in np.linspace(0, self.getDuration(), num=int(self.getDuration() * resolution)):
            pygame.draw.circle(screen, (20, 240, 15), toScreen(self.getPoseAtTime(time).tuple()), 1, 2)
        
    def compute(self):
        splines = []
        points = self.path.points()
        tangents = self.path.headings()

        for i in range(len(points) - 1):
            p0, p1 = points[i], points[i + 1]
            m0, m1 = tangents[i], tangents[i + 1]

            splines.append(Spline(p0, p1, m0, m1))  

        return splines