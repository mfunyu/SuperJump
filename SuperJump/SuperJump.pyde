#import global variables
add_library('minim')
from constants import *
# import class Game
from game import Game

player = Minim(this)

unmute = loadImage(PATH + "/images/unmute.png")
mute = loadImage(PATH + "/images/mute.png")
speaker = unmute

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
    image(speaker, 10, RESY - 100, 80, 80)


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
        game.play = True
        


def mouseClicked():
    global game

    game.play = True

def mousePressed():
    global bg_musics, speaker
    if ( 0 <= mouseX <= 100
        and RESY - 100 <= mouseY <= RESY):
        for music in bg_musics:
            if bg_musics[music].isMuted():
                bg_musics[music].unmute()
                speaker = unmute
            else:
                bg_musics[music].mute()
                speaker = mute
