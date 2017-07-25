# Slide Puizzle
# From Invent with Python
#craighole.com
#Creative Commons

import pygame, sys, random
from pygame.locals import *

# Create the constants (try different values)
BOARDWIDTH = int(input("Boardwidth>"))
BOARDHEIGHT = int(input("Boardheight>"))
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

#
BLACK = (0,0,0)
WHITE = (255,255,255)
BRIGHTBLUE = (0,50,255)
DARKTURQUOISE = (3,54,73)
GREEN = (0,204,0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE