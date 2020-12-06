#import global variables
add_library('minim')
from constants import *
# import class Game
from game import Game

player = Minim(this)

# instanciate game obj
bg_musics = {}
bg_musics['bg_music'] = player.loadFile(PATH + "/sounds/bg_music.mp3")
bg_musics['lose_life'] = player.loadFile(PATH + "/sounds/lose_life.mp3")

game = Game(bg_musics)

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
    if key == ' ':
        game.king.key_handler['jump'] = True


def keyReleased():
    global game

    if keyCode == LEFT:
        game.king.key_handler['left'] = False
    elif keyCode == RIGHT:
        game.king.key_handler['right'] = False
    if key == ' ':
        game.king.key_handler['jump'] = False


def mouseClicked():
    global game

    game.play = True
