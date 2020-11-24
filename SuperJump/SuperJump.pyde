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

    if keyCode == UP:
        game.tmp += 40
    if keyCode == RETURN:
        game.play = True
        
def mouseClicked():
    global game
            
    game.play = True
    
        
