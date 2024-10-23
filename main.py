import pygame
import sys
from path import Path
from pose import Pose
from trajectory import Trajectory
import math

### 
# TODO:
# Make points draggable
# add tangent points 
# instead of points have arrows pointing in inline [DONE] -> Works for the first spline but following splines falls apart
# connect splines via smooth lines
# add curvature to the spline and trajectory 
# change the colors line on a specified range depending on the curvature of the line

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
    Pose((20, 20), math.pi/2),
    Pose((-40, 5), math.pi/3),
    Pose((-25, 50), math.pi/2)
    ])

#path.addPose(Pose(20, 20), math.pi/4) # Also able to add paths like this

traj = Trajectory(path)

print(traj.splines[0].dx(0.5), traj.splines[0].dy(0.5), traj.splines[0].getHeadingAtTime(0.5))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get current mouse position
    pos = pygame.mouse.get_pos()

    # Draw the background image
    screen.blit(background_image, (0, 0))
    #screen.blit()

    traj.drawTrajectory(pygame, screen, resolution=15)
    path.drawPath(pygame, screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()