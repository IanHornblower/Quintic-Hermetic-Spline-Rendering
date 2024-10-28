from pose import Pose
from cordconversion import toField, toScreen
from polynomials import *
from spline import Spline
import numpy as np
from draw import draw_arrow, draw_spline
from motionprofile import MotionProfile

class Trajectory:
    def __init__(self, path, maxVelo = 55, minVelo = 0, maxAccel = 40, minDecel = -30):
        self.path = path
        self.splines = self.compute()
        
        self.length = sum(spline.getLength() for spline in self.splines)

        self.motionProfile = MotionProfile(maxVelo, minDecel, maxAccel, minVelo, self.length)
        
        self.duration = self.motionProfile.duration

    def getPoseAtTime(self, time):
        baseTime = int(np.ceil(time))
        currentSpline = self.splines[baseTime - 1]
        parametrizedTime = baseTime - time

        return currentSpline.getPoseAtTime(parametrizedTime)

    def getHeadingAtTime(self, time):
        return self.getPoseAtTime(time).heading()

    def splineCount(self):
        return len(self.splines)
    
    # pygame only
    def drawTrajectory(self, pygame, screen, direction = False, line = True, curvatureMap = False, arrows_per_spline = 10, spline_resolution = 20): # TODO: make it not draw every single frame, and only on update
        if line:
            for spline in self.splines:
                draw_spline(pygame, screen, spline, resolution=spline_resolution, cordTranslation=toScreen, curvatureMap=curvatureMap)

        if direction:   
            for time in np.linspace(0, self.splineCount(), num=int(self.splineCount() * arrows_per_spline)):
                pose = self.getPoseAtTime(time)
                draw_arrow(pygame, screen, Pose(toScreen(pose.tuple()), pose.heading), size=10, width=2)
        
    def compute(self):
        splines = []
        points = self.path.points()
        tangents = self.path.headings()

        for i in range(len(points) - 1):
            p0, p1 = points[i], points[i + 1]
            m0, m1 = tangents[i], tangents[i + 1]

            splines.append(Spline(p0, p1, m0, m1))  

        return splines