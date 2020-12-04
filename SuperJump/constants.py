"""
Global variables shared with all the classes

"""

import os

PATH = os.getcwd()

# size of the screen
RESX = 900 
RESY = RESX * 2/3

# king size
KING_SIZE = RESY / 8

# left boundary
GAMEX_L = RESX * 0.05
# right boundary
GAMEX_R = RESX * 0.95
MAGMA_H = RESX * 0.02

GAME_SPEED = 5

JUMP_HIGHET = 300


NUM_BG_IMGS = 4
NUM_IMG_DIV = 1
NUM_PHASE = 1
