import pygame
import sys
from path import Path
from pose import Pose
from spline import Spline
from trajectory import Trajectory
import math

### 
# TODO:
# add trajectory constraints 
# add desired velocity at time
# find a dif way to integrate
# make path points prettier
# make points draggable
# add tangent points
# clean up and optimze code

# Initialize Pygame
pygame.init()
pygame.font.init()

# Set the window size (1080x1080)
window_size = (640, 640)
screen = pygame.display.set_mode(window_size)

# Set the window title
pygame.display.set_caption('Path testing')

# Load and scale background image
background_image = pygame.image.load('field.png')
background_image = pygame.transform.scale(background_image, window_size)

running = True

path = Path([
    Pose((-40, -40), 0),
    Pose((40, -20), math.pi/4),
    Pose((20, 20), math.pi),
    Pose((-40, 19), math.pi/3),
    Pose((-25, 50), math.pi/6),
    Pose((30, 60), math.pi/1.2)
    ])

#path.addPose(Pose(20, 20), math.pi/4) # Also able to add paths like this

traj = Trajectory(path)

s = Spline((-25, 50), (30, 60), math.pi/6, math.pi/1.2)

print(s.length, s.getCurvature(0.5), s.getVelocityReduction(0.5))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get current mouse position
    pos = pygame.mouse.get_pos()

    # Draw the background image
    screen.blit(background_image, (0, 0))
    #screen.blit()

    traj.drawTrajectory(pygame, screen, arrows_per_spline=10, direction=False, curvatureMap=True)
    path.drawPath(pygame, screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()