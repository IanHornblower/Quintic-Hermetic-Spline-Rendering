from cordconversion import toField, toScreen
from pose import Pose

class Path:
    def __init__(self, path, pointColor=(200, 25, 25)):
        self.pointColor = pointColor
        self.path = path

    def addPose(self, pose: Pose):
        self.path.append(pose)

    def clearPath(self):
        self.path = []

    def list(self):
        return self.path

    def points(self):
        points = []

        for pose in self.path:
            points.append(pose.tuple())

        return points
    
    def headings(self):
        headings = []

        for pose in self.path:
            headings.append(pose.getHeading())

        return headings

    def drawPath(self, pygame, screen):  # TODO: make it not draw every single frame, and only on update
        for pose in self.path:
            pygame.draw.circle(screen, self.pointColor, toScreen(pose.tuple()), 2, 3)
            
