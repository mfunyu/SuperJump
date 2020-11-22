#import global variables
from constants import *
# import class Game
from game import Game

# instanciate game obj
game = Game()

def setup():
    size(RESX, RESY)
    background(0)

def draw():
    background(0)
    game.display()
    

def keyPressed():
    global game
    
    if keyCode == UP:
        game.p += 40
