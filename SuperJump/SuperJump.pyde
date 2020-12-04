#import global variables
from constants import *
# import class Game
from game import Game

# instanciate game obj
game = Game()

def setup():
    size(RESX, RESY)
    background(0)
    game.startup()

def draw():
    if game.play:
        game.display()


def keyPressed():
    global game

    if keyCode == LEFT:
        game.king.key_handler['left'] = True
    elif keyCode == RIGHT:
        game.king.key_handler['right'] = True
    if keyCode == UP:
        game.king.key_handler['jump'] = True


def keyReleased():
    global game

    if keyCode == LEFT:
        game.king.key_handler['left'] = False
    elif keyCode == RIGHT:
        game.king.key_handler['right'] = False
    if keyCode == UP:
        game.king.key_handler['jump'] = False


def mouseClicked():
    global game

    game.play = True


