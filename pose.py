import math

class Pose:
    def __init__(self, point, heading):
        self.x = point[0]
        self.y = point[1]
        self.heading = heading

    def x(self):
        return self.x

    def y(self):
        return self.y

    def tuple(self):
        return self.x,self.y

    def getHeading(self):
        return self.heading

    def __str__(self) -> str:
        return f"x: {self.x}, y: {self.y}, heading: {math.degrees(self.heading)}"