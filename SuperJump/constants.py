import os

PATH = os.getcwd()

# size of the screen
RESX = 900
RESY = RESX * 2/3

# king size
KING_SIZE = RESY / 8

# boundaries
GAMEX_L = RESX * 0.05
GAMEX_R = RESX * 0.95
GAMEX_U = RESY * 0.05
GAMEX_D = RESY * 0.95


MAGMA_H = RESX * 0.02

GAME_SPEED = 3

HORIZONTAL_MAX = 200
JUMP_HIGHET = 20


NUM_BG_IMGS = 5
NUM_IMG_DIV = 1
NUM_PHASE = 1

# loading flags
NOT_STARTED = 1 << 0
LOADING = 1 << 1
LOADED = 1 << 2
