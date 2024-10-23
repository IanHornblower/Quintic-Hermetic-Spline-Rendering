import pygame
from pose import Pose
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