import pygame
from spline import Spline
import numpy as np
from pose import Pose
from cordconversion import *
import math

def draw_arrow(pygame: pygame, screen, pose: Pose, color=(0, 150, 150), size=5, width=2):
    theta = 2*math.pi - pose.heading
    center = pose.tuple()
    
    tip = ((size / 2 * math.cos(theta)) + center[0], center[1] + (size / 2 * math.sin(theta)))

    edges = [
        (tip[0] + 0.7 * size * math.cos(theta + 3/4*math.pi), tip[1] + 0.7 * size * math.sin(theta + 3/4*math.pi)),
        (tip[0] + 0.7 * size * math.cos(theta - 3/4*math.pi), tip[1] + 0.7 * size * math.sin(theta - 3/4*math.pi))
    ]

    pygame.draw.lines(screen, color, False, [edges[0], tip, edges[1]], width=width)

def draw_spline(pygame: pygame, screen, spline: Spline, color = (255, 255, 255), resolution = 20, width = 2, cordTranslation = None):
    if cordTranslation != None:
        lastPoint = cordTranslation(spline.getPointAtTime(0))
    else: 
        lastPoint = spline.getPointAtTime(0)
    
    for time in np.linspace(0, 1, resolution):
        if cordTranslation != None:
            point = cordTranslation(spline.getPointAtTime(time))
        else: 
            point = spline.getPointAtTime(time)
        
        pygame.draw.line(screen, color, lastPoint, point, width)
        lastPoint = point