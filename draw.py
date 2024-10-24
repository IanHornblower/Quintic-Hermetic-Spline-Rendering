import pygame
from spline import Spline
import numpy as np
from pose import Pose
from cordconversion import *
import math
from pygame import Color
import colorsys

def draw_arrow(pygame: pygame, screen, pose: Pose, color=(0, 150, 150), size=5, width=2):
    theta = 2*math.pi - pose.heading
    center = pose.tuple()
    
    tip = ((size / 2 * math.cos(theta)) + center[0], center[1] + (size / 2 * math.sin(theta)))

    edges = [
        (tip[0] + 0.7 * size * math.cos(theta + 3/4*math.pi), tip[1] + 0.7 * size * math.sin(theta + 3/4*math.pi)),
        (tip[0] + 0.7 * size * math.cos(theta - 3/4*math.pi), tip[1] + 0.7 * size * math.sin(theta - 3/4*math.pi))
    ]

    pygame.draw.lines(screen, color, False, [edges[0], tip, edges[1]], width=width)

def draw_spline(pygame: pygame, screen, spline: Spline, color = (255, 0, 0), resolution = 20, width = 2, cordTranslation = None, curvatureMap = False):
    if cordTranslation != None:
        lastPoint = cordTranslation(spline.getPointAtTime(0))
    else: 
        lastPoint = spline.getPointAtTime(0)
    
    for time in np.linspace(0, 1, resolution):
        if cordTranslation != None:
            point = cordTranslation(spline.getPointAtTime(time))
        else: 
            point = spline.getPointAtTime(time)
        
        if curvatureMap:
            pygame.draw.line(screen, color_lerp((255, 0, 0), (0, 255, 0), spline.getVelocityReduction(time)), lastPoint, point, width)
        else:
            pygame.draw.line(screen, color, lastPoint, point, width)
        
        lastPoint = point

def lerp(a, b, t):
    return a + t * (b - a)

# Lifted from https://www.alanzucconi.com/2016/01/06/colour-interpolation/
def color_lerp(color_a, color_b, t):
    # Convert RGB to HSV
    color_a = Color(color_a)
    color_b = Color(color_b)
    a_hsv = colorsys.rgb_to_hsv(color_a[0], color_a[1], color_a[2])
    b_hsv = colorsys.rgb_to_hsv(color_b[0], color_b[1], color_b[2])

    # Hue interpolation
    h_a, s_a, v_a = a_hsv
    h_b, s_b, v_b = b_hsv
    
    d = h_b - h_a
    if h_a > h_b:
        h_a, h_b = h_b, h_a
        d = -d
        t = 1 - t

    if d > 0.5:  # Hue distance > 180 degrees
        h_a += 1  # Wrap around the hue
        h = (h_a + t * (h_b - h_a)) % 1
    else:
        h = h_a + t * d

    # Interpolate saturation, value, and alpha
    s = lerp(s_a, s_b, t)
    v = lerp(v_a, v_b, t)

    # Convert HSV back to RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    
    return (r, g, b)